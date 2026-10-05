"""Project backup export / restore (JSON or ZIP containing project.json)."""

from __future__ import annotations

import json
import zipfile
from datetime import datetime, timedelta
from io import BytesIO

from django.utils import timezone

from X.models import (
    Appointment,
    Appointment2Scene,
    Audio,
    Gadget,
    Location,
    Note,
    Person,
    Project,
    Role,
    Scene,
    SceneItem,
    Script,
    SFX,
    Shot,
    Time,
)

BACKUP_FORMAT = 'scriptumx-backup'
BACKUP_VERSION = 1


def _dt(value):
    if value is None:
        return None
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.isoformat()


def _parse_dt(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    if timezone.is_naive(parsed) and timezone.is_aware(timezone.now()):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _duration(value):
    if value is None:
        return None
    if isinstance(value, timedelta):
        return value.total_seconds()
    return None


def _parse_duration(value):
    if value is None or value == '':
        return None
    try:
        return timedelta(seconds=float(value))
    except (TypeError, ValueError):
        return None


def _base_fields(obj):
    data = {
        'id': obj.id,
        'name': obj.name,
        'abstract': obj.abstract,
        'description': obj.description,
    }
    for i in range(1, 13):
        data[f'tag{i}'] = getattr(obj, f'tag{i}')
    data['note_id'] = obj.note_id
    return data


def _apply_base_fields(obj, data):
    obj.name = (data.get('name') or '')[:50]
    obj.abstract = data.get('abstract') or ''
    obj.description = data.get('description') or ''
    for i in range(1, 13):
        setattr(obj, f'tag{i}', bool(data.get(f'tag{i}', False)))


def export_project(project):
    """Serialize a Project and related production data to a JSON-ready dict."""
    notes = {
        n.id: {
            'id': n.id,
            'text': n.text,
            'created': _dt(n.created),
            'author': n.author.username if n.author_id else None,
        }
        for n in Note.objects.filter(project=project)
    }

    def entity_list(model):
        rows = []
        for obj in model.objects.filter(project=project).order_by('name', 'id'):
            row = _base_fields(obj)
            rows.append(row)
        return rows

    roles = []
    for obj in Role.objects.filter(project=project).order_by('name', 'id'):
        row = _base_fields(obj)
        row['color'] = obj.color
        row['actor_id'] = obj.actor_id
        row['gadget_ids'] = list(obj.gadgets.values_list('id', flat=True))
        roles.append(row)

    persons = []
    for obj in Person.objects.filter(project=project).order_by('name', 'id'):
        row = _base_fields(obj)
        row['pervasive'] = obj.pervasive
        row['contact'] = obj.contact
        row['email'] = obj.email
        row['costs'] = obj.costs
        persons.append(row)

    locations = entity_list(Location)
    times = entity_list(Time)

    gadgets = []
    for obj in Gadget.objects.filter(project=project).order_by('name', 'id'):
        row = _base_fields(obj)
        row['pervasive'] = obj.pervasive
        row['progress'] = obj.progress
        row['costs'] = obj.costs
        gadgets.append(row)

    audios = []
    for obj in Audio.objects.filter(project=project).order_by('name', 'id'):
        row = _base_fields(obj)
        row['progress'] = obj.progress
        row['costs'] = obj.costs
        audios.append(row)

    sfxs = []
    for obj in SFX.objects.filter(project=project).order_by('name', 'id'):
        row = _base_fields(obj)
        row['progress'] = obj.progress
        row['costs'] = obj.costs
        sfxs.append(row)

    scripts = []
    for script in Script.objects.filter(project=project).order_by('id'):
        scenes = []
        for scene in Scene.objects.filter(project=project, script=script).order_by('order', 'id'):
            items = []
            for item in SceneItem.objects.filter(scene=scene).order_by('order', 'id'):
                shots = []
                for shot in Shot.objects.filter(sceneitem=item).order_by('column', 'id'):
                    shots.append({
                        'id': shot.id,
                        'name': shot.name,
                        'column': shot.column,
                        'length': shot.length,
                        'cam_field_size': shot.cam_field_size,
                        'cam_angle': shot.cam_angle,
                        'description': shot.description,
                    })
                items.append({
                    'id': item.id,
                    'order': item.order,
                    'type': item.type,
                    'parenthetical': item.parenthetical,
                    'text': item.text,
                    'role_id': item.role_id,
                    'updated_at': _dt(getattr(item, 'updated_at', None)),
                    'shots': shots,
                })
            scenes.append({
                'id': scene.id,
                'order': scene.order,
                'short': scene.short,
                'indentation': scene.indentation,
                'color': scene.color,
                'duration': _duration(scene.duration),
                'progress_script': scene.progress_script,
                'progress_pre': scene.progress_pre,
                'progress_shot': scene.progress_shot,
                'progress_post': scene.progress_post,
                'story_location_id': scene.story_location_id,
                'story_time_id': scene.story_time_id,
                'person_ids': list(scene.persons.values_list('id', flat=True)),
                'gadget_ids': list(scene.gadgets.values_list('id', flat=True)),
                'audio_ids': list(scene.audios.values_list('id', flat=True)),
                'sfx_ids': list(scene.sfxs.values_list('id', flat=True)),
                'updated_at': _dt(getattr(scene, 'updated_at', None)),
                'sceneitems': items,
                **_base_fields(scene),
            })
        scripts.append({
            'id': script.id,
            'name': script.name,
            'abstract': script.abstract,
            'description': script.description,
            'author': script.author,
            'version': script.version,
            'copyright': script.copyright,
            'person_ids': list(script.persons.values_list('id', flat=True)),
            'scenes': scenes,
        })

    appointments = []
    for appt in Appointment.objects.filter(project=project).order_by('id'):
        row = _base_fields(appt)
        row.update({
            'time_all': _dt(appt.time_all),
            'duration_all': _duration(appt.duration_all),
            'meeting_point_id': appt.meeting_point_id,
            'person_ids': list(appt.persons.values_list('id', flat=True)),
            'gadget_ids': list(appt.gadgets.values_list('id', flat=True)),
            'scene_ids': list(
                Appointment2Scene.objects.filter(appointment=appt)
                .values_list('scene_id', flat=True)
            ),
        })
        appointments.append(row)

    return {
        'format': BACKUP_FORMAT,
        'version': BACKUP_VERSION,
        'exported_at': _dt(timezone.now()),
        'project': {
            'id': project.id,
            'name': project.name,
        },
        'notes': list(notes.values()),
        'roles': roles,
        'persons': persons,
        'locations': locations,
        'times': times,
        'gadgets': gadgets,
        'audios': audios,
        'sfxs': sfxs,
        'scripts': scripts,
        'appointments': appointments,
    }


def dumps_project(project, indent=2):
    return json.dumps(export_project(project), indent=indent, ensure_ascii=False)


def zip_project(project):
    """Return ZIP bytes containing project.json."""
    payload = dumps_project(project).encode('utf-8')
    buf = BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        safe_name = ''.join(c if c.isalnum() or c in '-_' else '_' for c in project.name) or 'project'
        zf.writestr(f'{safe_name}.json', payload)
        zf.writestr('project.json', payload)
    return buf.getvalue()


def load_backup_bytes(raw, filename=''):
    """Parse uploaded JSON or ZIP bytes into a backup dict."""
    name = (filename or '').lower()
    if name.endswith('.zip') or (len(raw) >= 2 and raw[:2] == b'PK'):
        with zipfile.ZipFile(BytesIO(raw), 'r') as zf:
            # Prefer project.json, else first .json
            names = zf.namelist()
            target = None
            if 'project.json' in names:
                target = 'project.json'
            else:
                for n in names:
                    if n.lower().endswith('.json') and not n.endswith('/'):
                        target = n
                        break
            if not target:
                raise ValueError('ZIP backup has no JSON payload')
            raw = zf.read(target)
    if isinstance(raw, bytes):
        text = raw.decode('utf-8')
    else:
        text = raw
    data = json.loads(text)
    if not isinstance(data, dict) or data.get('format') != BACKUP_FORMAT:
        raise ValueError('Not a ScriptumX backup file')
    return data


def restore_project(data, owner, name_suffix=' (restored)'):
    """Create a new Project from backup dict owned by ``owner``."""
    if data.get('format') != BACKUP_FORMAT:
        raise ValueError('Unsupported backup format')

    src = data.get('project') or {}
    base_name = (src.get('name') or 'Restored Project')[:50]
    project_name = (base_name + name_suffix)[:50]
    project = Project.objects.create(name=project_name, owner=owner)

    note_map = {}
    for nd in data.get('notes') or []:
        note = Note(project=project, text=nd.get('text') or '', author=owner)
        created = _parse_dt(nd.get('created'))
        note.save()
        if created:
            Note.objects.filter(pk=note.pk).update(created=created)
            note.refresh_from_db()
        note_map[nd.get('id')] = note

    def create_entities(model, rows):
        mapping = {}
        for row in rows or []:
            obj = model(project=project)
            _apply_base_fields(obj, row)
            old_note = row.get('note_id')
            if old_note in note_map:
                obj.note = note_map[old_note]
            obj.save()
            mapping[row.get('id')] = obj
        return mapping

    person_map = {}
    for row in data.get('persons') or []:
        obj = Person(project=project)
        _apply_base_fields(obj, row)
        obj.pervasive = bool(row.get('pervasive', False))
        obj.contact = row.get('contact') or ''
        obj.email = (row.get('email') or '')[:254]
        obj.costs = int(row.get('costs') or 0)
        old_note = row.get('note_id')
        if old_note in note_map:
            obj.note = note_map[old_note]
        obj.save()
        person_map[row.get('id')] = obj

    gadget_map = {}
    for row in data.get('gadgets') or []:
        obj = Gadget(project=project)
        _apply_base_fields(obj, row)
        obj.pervasive = bool(row.get('pervasive', False))
        obj.progress = int(row.get('progress') or 0)
        obj.costs = int(row.get('costs') or 0)
        old_note = row.get('note_id')
        if old_note in note_map:
            obj.note = note_map[old_note]
        obj.save()
        gadget_map[row.get('id')] = obj

    audio_map = {}
    for row in data.get('audios') or []:
        obj = Audio(project=project)
        _apply_base_fields(obj, row)
        obj.progress = int(row.get('progress') or 0)
        obj.costs = int(row.get('costs') or 0)
        old_note = row.get('note_id')
        if old_note in note_map:
            obj.note = note_map[old_note]
        obj.save()
        audio_map[row.get('id')] = obj

    sfx_map = {}
    for row in data.get('sfxs') or []:
        obj = SFX(project=project)
        _apply_base_fields(obj, row)
        obj.progress = int(row.get('progress') or 0)
        obj.costs = int(row.get('costs') or 0)
        old_note = row.get('note_id')
        if old_note in note_map:
            obj.note = note_map[old_note]
        obj.save()
        sfx_map[row.get('id')] = obj

    location_map = create_entities(Location, data.get('locations'))
    time_map = create_entities(Time, data.get('times'))

    role_map = {}
    for row in data.get('roles') or []:
        obj = Role(project=project)
        _apply_base_fields(obj, row)
        obj.color = row.get('color') or '#FFFFFF'
        actor_id = row.get('actor_id')
        if actor_id in person_map:
            obj.actor = person_map[actor_id]
        old_note = row.get('note_id')
        if old_note in note_map:
            obj.note = note_map[old_note]
        obj.save()
        obj.gadgets.set([gadget_map[i] for i in (row.get('gadget_ids') or []) if i in gadget_map])
        role_map[row.get('id')] = obj

    scene_map = {}
    for sd in data.get('scripts') or []:
        script = Script.objects.create(
            project=project,
            name=(sd.get('name') or 'Script')[:50],
            abstract=sd.get('abstract') or '',
            description=sd.get('description') or '',
            author=(sd.get('author') or '')[:300],
            version=(sd.get('version') or '')[:50],
            copyright=(sd.get('copyright') or '')[:300],
        )
        person_ids = [person_map[i] for i in (sd.get('person_ids') or []) if i in person_map]
        if person_ids:
            script.persons.set(person_ids)

        for sc in sd.get('scenes') or []:
            scene = Scene(project=project, script=script)
            _apply_base_fields(scene, sc)
            scene.order = int(sc.get('order') or 0)
            scene.short = (sc.get('short') or '')[:5]
            scene.indentation = int(sc.get('indentation') or 0)
            scene.color = sc.get('color') or '#FFFFFF'
            scene.duration = _parse_duration(sc.get('duration'))
            scene.progress_script = int(sc.get('progress_script') or 0)
            scene.progress_pre = int(sc.get('progress_pre') or 0)
            scene.progress_shot = int(sc.get('progress_shot') or 0)
            scene.progress_post = int(sc.get('progress_post') or 0)
            loc_id = sc.get('story_location_id')
            time_id = sc.get('story_time_id')
            if loc_id in location_map:
                scene.story_location = location_map[loc_id]
            if time_id in time_map:
                scene.story_time = time_map[time_id]
            old_note = sc.get('note_id')
            if old_note in note_map:
                scene.note = note_map[old_note]
            scene.save()
            scene_map[sc.get('id')] = scene
            scene.persons.set([person_map[i] for i in (sc.get('person_ids') or []) if i in person_map])
            scene.gadgets.set([gadget_map[i] for i in (sc.get('gadget_ids') or []) if i in gadget_map])
            scene.audios.set([audio_map[i] for i in (sc.get('audio_ids') or []) if i in audio_map])
            scene.sfxs.set([sfx_map[i] for i in (sc.get('sfx_ids') or []) if i in sfx_map])

            for it in sc.get('sceneitems') or []:
                item = SceneItem(
                    scene=scene,
                    order=int(it.get('order') or 0),
                    type=(it.get('type') or '')[:1],
                    parenthetical=(it.get('parenthetical') or '')[:100],
                    text=it.get('text') or '',
                )
                role_id = it.get('role_id')
                if role_id in role_map:
                    item.role = role_map[role_id]
                item.save()
                for sh in it.get('shots') or []:
                    Shot.objects.create(
                        sceneitem=item,
                        scene=scene,
                        name=(sh.get('name') or '')[:50],
                        column=int(sh.get('column') or 0),
                        length=int(sh.get('length') or 1),
                        cam_field_size=(sh.get('cam_field_size') or '')[:5],
                        cam_angle=(sh.get('cam_angle') or '')[:5],
                        description=sh.get('description') or '',
                    )

    for ap in data.get('appointments') or []:
        appt = Appointment(project=project)
        _apply_base_fields(appt, ap)
        appt.time_all = _parse_dt(ap.get('time_all'))
        appt.duration_all = _parse_duration(ap.get('duration_all'))
        mp = ap.get('meeting_point_id')
        if mp in location_map:
            appt.meeting_point = location_map[mp]
        old_note = ap.get('note_id')
        if old_note in note_map:
            appt.note = note_map[old_note]
        appt.save()
        appt.persons.set([person_map[i] for i in (ap.get('person_ids') or []) if i in person_map])
        appt.gadgets.set([gadget_map[i] for i in (ap.get('gadget_ids') or []) if i in gadget_map])
        for scene_id in ap.get('scene_ids') or []:
            if scene_id in scene_map:
                Appointment2Scene.objects.create(appointment=appt, scene=scene_map[scene_id])

    return project
