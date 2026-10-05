from django.contrib import admin

from report.models import FilterPreset, ReportShareLink


@admin.register(ReportShareLink)
class ReportShareLinkAdmin(admin.ModelAdmin):
    list_display = ('token', 'report_name', 'project', 'label', 'created_by', 'created_at', 'revoked', 'expires_at')
    list_filter = ('report_name', 'revoked')
    search_fields = ('token', 'label', 'title')
    readonly_fields = ('token', 'created_at')


@admin.register(FilterPreset)
class FilterPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'tag_group', 'report_name', 'updated_at')
    list_filter = ('tag_group',)
    search_fields = ('name', 'user__username')
