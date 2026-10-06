"""Conflict helpers for Scene / SceneItem editors."""

from django.utils.dateparse import parse_datetime


def token_for(obj):
    """Stable string token for an object's updated_at (or empty)."""
    value = getattr(obj, 'updated_at', None)
    if not value:
        return ''
    return value.isoformat()


def is_stale(obj, expected_token):
    """True when expected_token is set and does not match current updated_at."""
    if not expected_token:
        return False
    current = token_for(obj)
    if not current:
        return False
    # Normalize both sides via parse when possible
    expected = expected_token
    parsed = parse_datetime(expected_token)
    if parsed is not None:
        expected = parsed.isoformat()
        current = obj.updated_at.isoformat()
    return expected != current
