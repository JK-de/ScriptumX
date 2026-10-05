"""
Script importers: Celtx, Fountain, Final Draft (.fdx), and plain text.
"""
from __future__ import annotations

import html
import re
import zipfile
from datetime import datetime
from io import BytesIO
from xml.etree import ElementTree as ET

from X.models import Gadget, Location, Project, Role, Scene, SceneItem, Script, SFX


SCENE_HEADING_RE = re.compile(
    r'^\s*(INT\.?/EXT\.?|INT\.?|EXT\.?|I/?E\.?|EST\.?|ESTABLISHING)\b',
    re.IGNORECASE,
)
TRANSITION_RE = re.compile(
    r'^\s*(FADE (IN|OUT)|CUT TO|DISSOLVE TO|SMASH CUT TO|MATCH CUT TO|JUMP CUT TO|'
    r'WIPE TO|IRIS (IN|OUT)|TO BLACK|TO WHITE).*:?\s*$',
    re.IGNORECASE,
)
FORCE_SCENE_RE = re.compile(r'^\s*\.(?P<title>\S.+)$')
FORCE_CHARACTER_RE = re.compile(r'^\s*@(?P<name>.+)$')


def detect_format(filename: str, data: bytes) -> str:
    """Guess import format from filename and content sniffing."""
    name = (filename or '').lower()
    text_head = ''
    try:
        text_head = data[:4000].decode('utf-8', 'ignore')
    except Exception:
        text_head = ''

    if name.endswith('.celtx') or (len(data) >= 2 and data[0:2] == b'PK' and b'script' in data[:8000]):
        return 'celtx'
    if name.endswith('.fdx') or '<FinalDraft' in text_head or '<Paragraph Type=' in text_head:
        return 'fdx'
    if name.endswith('.fountain') or name.endswith('.spmd'):
        return 'fountain'
    if name.endswith('.txt') or name.endswith('.text'):
        if 'class="sceneheading"' in text_head or 'class="action"' in text_head:
            return 'celtx'
        return 'plain'
    if 'class="sceneheading"' in text_head:
        return 'celtx'
    return 'fountain'


def _strip_html(value: str) -> str:
    value = re.sub(r'<br\s*/?>', '\n', value, flags=re.IGNORECASE)
    value = re.sub(r'<[^>]+>', '', value)
    return html.unescape(value).strip()


def _entity_name(text: str, fallback: str = 'Item') -> str:
    cleaned = _strip_html(text or '')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if not cleaned:
        cleaned = fallback
    return cleaned[:50]


class ImporterBase:
    """Shared helpers that create Script / Scene / SceneItem / Role records."""

    env = None
    sceneItem_counter = 1
    scene_counter = 1

    def __init__(self, env, *args, **kwargs):
        self.env = env
        self.sceneItem_counter = 1
        self.scene_counter = 1

    def getRole(self, name):
        if name is None:
            name = '<unknown>'
        name = name[:50]
        try:
            role = Role.objects.get(project=self.env.project, name__iexact=name)
        except Role.DoesNotExist:
            role = Role(name=name, project=self.env.project)
            role.save()
        return role

    def getLocation(self, name):
        if name is None:
            name = '<unknown>'
        name = name[:50]
        try:
            location = Location.objects.get(project=self.env.project, name__iexact=name)
        except Location.DoesNotExist:
            location = Location(name=name, project=self.env.project)
            location.save()
        return location

    def getGadget(self, name):
        name = _entity_name(name, 'Prop')
        try:
            gadget = Gadget.objects.get(project=self.env.project, name__iexact=name)
        except Gadget.DoesNotExist:
            gadget = Gadget(name=name, project=self.env.project)
            gadget.save()
        return gadget

    def getSFX(self, name):
        name = _entity_name(name, 'SFX')
        try:
            sfx = SFX.objects.get(project=self.env.project, name__iexact=name)
        except SFX.DoesNotExist:
            sfx = SFX(name=name, project=self.env.project)
            sfx.save()
        return sfx

    def addScene(self, name):
        if name is None:
            name = '<unknown>'
        name = name[:50]
        self.sceneItem_counter = 1
        scene = Scene()
        scene.setAllTags(True)
        scene.name = name
        scene.project = self.env.project
        scene.script = self.env.script
        scene.order = self.scene_counter
        self.scene_counter += 1
        scene.save()
        self.env.setScene(scene)
        return scene

    def addScript(self, name, abstract=''):
        if name is None:
            name = '<unknown>'
        name = name[:50]
        script = Script()
        script.name = name
        script.abstract = abstract
        script.project = self.env.project
        script.revision_label = 'White'
        script.revision_color = '#FFFFFF'
        script.save()
        self.env.setScript(script)
        return script

    def addSceneItem(self, type, role_name, parenthetical, text):
        sceneItem = SceneItem()
        sceneItem.type = type
        if role_name:
            sceneItem.role = self.getRole(role_name[:50])
        else:
            sceneItem.role = None
        sceneItem.parenthetical = (parenthetical or '')[:100]
        sceneItem.text = text or ''
        sceneItem.scene = self.env.scene
        sceneItem.order = self.sceneItem_counter
        self.sceneItem_counter += 1
        sceneItem.save()
        return sceneItem

    def ensure_scene(self):
        if not self.env.scene:
            self.addScene('UNTITLED SCENE')

    def import_celtx_html(self, data: str):
        pattern = re.compile(
            r'''
            <p
            .*?
            class="(?P<key>.*?)"
            .*?
            >
            (?P<value>.*?)
            </p>
            ''',
            re.VERBOSE | re.MULTILINE | re.DOTALL,
        )
        pattern_ws = r'&nbsp;|<br>|\n|:$'
        act_role = None
        act_parenthetical = ''

        for match in re.finditer(pattern, data):
            key = match.group('key')
            value_raw = match.group('value')
            value = re.sub(pattern_ws, r' ', value_raw).strip()
            if not value:
                continue

            value = re.sub(r'<span style="font-weight: bold;">(.*?)</span>', r'<b>\1</b>', value)
            value = re.sub(
                r'<span style="text-decoration: underline;">(.*?)</span>', r'<u>\1</u>', value
            )
            value = html.unescape(value)
            value = value.replace('´', "'")

            if key == 'action':
                self.ensure_scene()
                self.addSceneItem('A', None, '', value)
            elif key == 'character':
                value = re.sub(r'\s+', r' ', value).rstrip(':')
                act_role = value
            elif key == 'parenthetical':
                act_parenthetical = value
            elif key == 'dialog':
                self.ensure_scene()
                self.addSceneItem('D', act_role, act_parenthetical, value)
                act_parenthetical = ''
            elif key == 'sceneheading':
                self.addScene(value)
            elif key in ('shot', 'transition'):
                pass

    def import_fountain_lines(self, lines):
        """Parse Fountain / screenplay plain-text lines into scenes and items."""
        act_role = None
        act_parenthetical = ''
        expecting_dialogue = False

        for raw in lines:
            line = raw.rstrip('\r\n')
            stripped = line.strip()
            if not stripped:
                act_role = None
                act_parenthetical = ''
                expecting_dialogue = False
                continue

            # Boneyard / notes / title page keys — skip lightly
            if stripped.startswith('/*') or stripped.startswith('[[') or stripped.startswith('='):
                continue
            if ':' in stripped and stripped.split(':', 1)[0].isupper() and len(stripped.split(':', 1)[0]) < 20:
                # title-page style KEY: value
                key = stripped.split(':', 1)[0]
                if key in ('Title', 'Author', 'Draft date', 'Contact', 'Copyright'):
                    continue

            force_scene = FORCE_SCENE_RE.match(stripped)
            if force_scene:
                self.addScene(force_scene.group('title').strip())
                expecting_dialogue = False
                continue

            if SCENE_HEADING_RE.match(stripped) or (
                stripped.isupper() and SCENE_HEADING_RE.match(stripped)
            ):
                self.addScene(stripped)
                expecting_dialogue = False
                continue

            if TRANSITION_RE.match(stripped) or (
                stripped.isupper() and stripped.endswith('TO:')
            ):
                self.ensure_scene()
                self.addSceneItem('T', None, '', stripped)
                expecting_dialogue = False
                continue

            force_char = FORCE_CHARACTER_RE.match(stripped)
            if force_char:
                act_role = force_char.group('name').strip()
                expecting_dialogue = True
                continue

            if stripped.startswith('(') and stripped.endswith(')') and expecting_dialogue:
                act_parenthetical = stripped.strip('()')
                continue

            # Character cue: short ALL CAPS line
            if (
                stripped.isupper()
                and len(stripped) <= 40
                and not stripped.endswith('.')
                and not SCENE_HEADING_RE.match(stripped)
            ):
                act_role = stripped.rstrip('^').strip()
                expecting_dialogue = True
                continue

            self.ensure_scene()
            if expecting_dialogue and act_role:
                self.addSceneItem('D', act_role, act_parenthetical, stripped)
                act_parenthetical = ''
                # stay in dialogue block until blank line
            else:
                self.addSceneItem('A', None, '', stripped)
                expecting_dialogue = False

    def import_fdx(self, data: str):
        # Final Draft XML may include a default namespace
        root = ET.fromstring(data)
        act_role = None
        act_parenthetical = ''

        paragraphs = root.findall('.//{*}Paragraph')
        if not paragraphs:
            paragraphs = root.findall('.//Paragraph')

        for para in paragraphs:
            ptype = (para.get('Type') or '').strip()
            texts = []
            for text_el in para.findall('.//{*}Text'):
                if text_el.text:
                    texts.append(text_el.text)
            if not texts:
                for text_el in para.findall('.//Text'):
                    if text_el.text:
                        texts.append(text_el.text)
            value = ''.join(texts).strip()
            if not value and para.text:
                value = para.text.strip()
            if not value:
                continue

            if ptype in ('Scene Heading', 'Scene Heading'):
                self.addScene(value)
                act_role = None
                act_parenthetical = ''
            elif ptype == 'Action':
                self.ensure_scene()
                self.addSceneItem('A', None, '', value)
            elif ptype == 'Character':
                act_role = value
                act_parenthetical = ''
            elif ptype == 'Parenthetical':
                act_parenthetical = value.strip('()')
            elif ptype == 'Dialogue':
                self.ensure_scene()
                self.addSceneItem('D', act_role, act_parenthetical, value)
                act_parenthetical = ''
            elif ptype == 'Transition':
                self.ensure_scene()
                self.addSceneItem('T', None, '', value)

    def doImport(self, filename, data: bytes | None = None, fmt: str | None = None):
        if data is None:
            with open(filename, 'rb') as f:
                data = f.read()

        fmt = (fmt or 'auto').lower()
        if fmt in ('', 'auto'):
            fmt = detect_format(filename, data)

        label = {
            'celtx': 'celtx',
            'fountain': 'fountain',
            'fdx': 'final draft',
            'plain': 'plain text',
        }.get(fmt, fmt)

        script_name = 'IMPORT'
        base = (filename or 'import').rsplit('/', 1)[-1]
        if '.' in base:
            script_name = base.rsplit('.', 1)[0][:50] or 'IMPORT'

        self.addScript(
            script_name,
            'import from %s (%s) at %s' % (label, base, datetime.now()),
        )

        if fmt == 'celtx':
            text = self._read_celtx(data)
            self.import_celtx_html(text)
        elif fmt == 'fdx':
            text = data.decode('utf-8', 'ignore')
            if not text.strip():
                text = data.decode('cp1252', 'ignore')
            self.import_fdx(text)
        else:
            # fountain + plain share line parser
            text = data.decode('utf-8', 'ignore')
            if not text.strip():
                text = data.decode('cp1252', 'ignore')
            # normalize newlines and drop BOM
            text = text.lstrip('\ufeff').replace('\r\n', '\n').replace('\r', '\n')
            self.import_fountain_lines(text.split('\n'))

        return self.env.script

    def _read_celtx(self, data: bytes) -> str:
        """Celtx files are ZIP archives; fall back to raw HTML/text decode."""
        if len(data) >= 2 and data[0:2] == b'PK':
            try:
                with zipfile.ZipFile(BytesIO(data)) as zf:
                    # Prefer script HTML fragments inside the package
                    candidates = [
                        n for n in zf.namelist()
                        if n.lower().endswith(('.html', '.htm', '.celtx'))
                        or 'script' in n.lower()
                    ]
                    for name in candidates or zf.namelist():
                        raw = zf.read(name)
                        text = raw.decode('utf-8', 'ignore')
                        if not text.strip():
                            text = raw.decode('cp1252', 'ignore')
                        if 'class="' in text and '<p' in text:
                            return text
                    # last resort: concatenate decodable members
                    chunks = []
                    for name in zf.namelist():
                        raw = zf.read(name)
                        chunks.append(raw.decode('cp1252', 'ignore'))
                    return '\n'.join(chunks)
            except zipfile.BadZipFile:
                pass
        text = data.decode('cp1252', 'ignore')
        if not text.strip():
            text = data.decode('utf-8', 'ignore')
        return text
