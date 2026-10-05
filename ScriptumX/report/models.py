"""Report collaboration models: share links and filter presets."""
import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_share_token():
    return secrets.token_urlsafe(24)


class ReportShareLink(models.Model):
    """Tokenized, read-only link to a frozen report view (F14)."""

    token = models.CharField(max_length=64, unique=True, db_index=True, default=generate_share_token)
    project = models.ForeignKey('X.Project', on_delete=models.CASCADE, related_name='report_share_links')
    script = models.ForeignKey(
        'X.Script', on_delete=models.CASCADE, null=True, blank=True, related_name='report_share_links',
    )
    report_name = models.CharField(max_length=64, help_text='report URL name, e.g. L_Location')
    title = models.CharField(max_length=120, blank=True)
    label = models.CharField(max_length=100, blank=True)
    filter_payload = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='report_share_links',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.label or self.title or self.token

    def is_active(self):
        if self.revoked:
            return False
        if self.expires_at and self.expires_at <= timezone.now():
            return False
        return True


class FilterPreset(models.Model):
    """Named per-user filter snapshot for report/editor tag filters (F15)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filter_presets',
    )
    name = models.CharField(max_length=100)
    tag_group = models.CharField(max_length=32, help_text='e.g. location, scene, role')
    report_name = models.CharField(max_length=64, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = [('user', 'name', 'tag_group')]

    def __str__(self):
        return '%s (%s)' % (self.name, self.tag_group)
