# -*- coding: utf-8 -*-
"""Embedded Unicode PDF fonts and Google-font → local mapping for xhtml2pdf."""
from __future__ import annotations

import os
import re

# Bundled under report/static/report/fonts/ (DejaVu — Bitstream Vera license).
FONT_STATIC_PREFIX = 'report/fonts'

FACE_FILES = {
    'DejaVu Sans': {
        'normal': 'DejaVuSans.ttf',
        'bold': 'DejaVuSans-Bold.ttf',
    },
    'DejaVu Serif': {
        'normal': 'DejaVuSerif.ttf',
        'bold': 'DejaVuSerif-Bold.ttf',
    },
    'DejaVu Sans Mono': {
        'normal': 'DejaVuSansMono.ttf',
        'bold': 'DejaVuSansMono-Bold.ttf',
    },
}

DEFAULT_PDF_FAMILY = 'DejaVu Sans'

# Layout picker / CSS family names → embedded PDF family.
_FAMILY_ALIASES = {
    # System / web stacks
    'arial': 'DejaVu Sans',
    'helvetica': 'DejaVu Sans',
    'verdana': 'DejaVu Sans',
    'geneva': 'DejaVu Sans',
    'trebuchet ms': 'DejaVu Sans',
    'lucida sans unicode': 'DejaVu Sans',
    'lucida grande': 'DejaVu Sans',
    'times new roman': 'DejaVu Serif',
    'times': 'DejaVu Serif',
    'palatino linotype': 'DejaVu Serif',
    'book antiqua': 'DejaVu Serif',
    'palatino': 'DejaVu Serif',
    'courier new': 'DejaVu Sans Mono',
    'courier': 'DejaVu Sans Mono',
    'lucida console': 'DejaVu Sans Mono',
    'monaco': 'DejaVu Sans Mono',
    # Google fonts offered in ScriptFilterForm
    'amiri': 'DejaVu Serif',
    'lato': 'DejaVu Sans',
    'open sans': 'DejaVu Sans',
    'source sans pro': 'DejaVu Sans',
    'pt serif': 'DejaVu Serif',
    'pt sans': 'DejaVu Sans',
    'source serif pro': 'DejaVu Serif',
    'source code pro': 'DejaVu Sans Mono',
    'pt mono': 'DejaVu Sans Mono',
    'cutive mono': 'DejaVu Sans Mono',
    'alegreya sans': 'DejaVu Sans',
    'droid sans mono': 'DejaVu Sans Mono',
    'rambla': 'DejaVu Sans',
}

# google_link fragment (e.g. Open+Sans:400,...) → family
_GOOGLE_LINK_ALIASES = {
    'amiri': 'DejaVu Serif',
    'lato': 'DejaVu Sans',
    'open+sans': 'DejaVu Sans',
    'open sans': 'DejaVu Sans',
    'source+sans+pro': 'DejaVu Sans',
    'source sans pro': 'DejaVu Sans',
    'pt+serif': 'DejaVu Serif',
    'pt serif': 'DejaVu Serif',
    'pt+sans': 'DejaVu Sans',
    'pt sans': 'DejaVu Sans',
    'source+serif+pro': 'DejaVu Serif',
    'source serif pro': 'DejaVu Serif',
    'source+code+pro': 'DejaVu Sans Mono',
    'source code pro': 'DejaVu Sans Mono',
    'pt+mono': 'DejaVu Sans Mono',
    'pt mono': 'DejaVu Sans Mono',
    'cutive+mono': 'DejaVu Sans Mono',
    'cutive mono': 'DejaVu Sans Mono',
    'alegreya+sans': 'DejaVu Sans',
    'alegreya sans': 'DejaVu Sans',
    'droid+sans+mono': 'DejaVu Sans Mono',
    'droid sans mono': 'DejaVu Sans Mono',
    'rambla': 'DejaVu Sans',
}


def _normalize_family(name: str) -> str:
    return re.sub(r'\s+', ' ', name.strip().strip('"\'').lower())


def _first_css_family(font_stack: str) -> str:
    if not font_stack:
        return ''
    first = font_stack.split(',')[0].strip()
    return _normalize_family(first)


def resolve_pdf_font_family(font_stack: str = '', google_link: str = '') -> str:
    """
    Map a browser layout choice (CSS stack and/or Google Fonts link fragment)
    to an embedded DejaVu family name for PDF output.
    """
    if google_link:
        key = google_link.split(':', 1)[0].strip().lower().replace(' ', '+')
        mapped = _GOOGLE_LINK_ALIASES.get(key) or _GOOGLE_LINK_ALIASES.get(
            key.replace('+', ' ')
        )
        if mapped:
            return mapped

    first = _first_css_family(font_stack or '')
    if first in _FAMILY_ALIASES:
        return _FAMILY_ALIASES[first]
    # Already an embedded family name
    for family in FACE_FILES:
        if first == family.lower():
            return family
    return DEFAULT_PDF_FAMILY


def pdf_font_face_css(static_url: str = '/static/') -> str:
    """
    @font-face rules pointing at bundled TTFs.

    xhtml2pdf 0.2.x enforces a document-root resource policy and does not
    reliably resolve /static/... URLs for fonts, so we emit absolute filesystem
    paths under the project tree (allowed by the policy).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(here, 'static', 'report', 'fonts')
    rules = []
    for family, variants in FACE_FILES.items():
        for weight_name, filename in variants.items():
            weight = 'bold' if weight_name == 'bold' else 'normal'
            abs_path = os.path.join(font_dir, filename).replace('\\', '/')
            rules.append(
                '@font-face {\n'
                '  font-family: "%s";\n'
                '  src: url("%s");\n'
                '  font-weight: %s;\n'
                '  font-style: normal;\n'
                '}' % (family, abs_path, weight)
            )
    return '\n'.join(rules)


def bundled_font_paths():
    """Absolute paths to bundled TTFs (for tests / diagnostics)."""
    here = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(here, 'static', 'report', 'fonts')
    paths = []
    for variants in FACE_FILES.values():
        for filename in variants.values():
            paths.append(os.path.join(font_dir, filename))
    return paths
