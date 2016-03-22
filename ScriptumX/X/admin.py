"""
Customizations for the Django administration interface.
"""

from django.contrib import admin
from X.models import *


class ProjectAdmin(admin.ModelAdmin):
    """Definition of the Project editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_12M', {'fields': ['owner']}),
        ('_M2M', {'fields': ['users', 'readers']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name',)
    #list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Project, ProjectAdmin)

class NoteAdmin(admin.ModelAdmin):
    """Definition of the Note editor."""
    fieldsets = [
        (None, {'fields': ['text']}),
        ('_12M', {'fields': ['project', 'author']}),
    ]
    list_display = ('created', 'text', 'project')
    list_filter = ['project']
    search_fields = ['text']

admin.site.register(Note, NoteAdmin)

class GadgetAdmin(admin.ModelAdmin):
    """Definition of the Gadget editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Gadget, GadgetAdmin)

class AudioAdmin(admin.ModelAdmin):
    """Definition of the Audio editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Audio, AudioAdmin)

class SfxAdmin(admin.ModelAdmin):
    """Definition of the SFX editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(SFX, SfxAdmin)

class PersonAdmin(admin.ModelAdmin):
    """Definition of the Person editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['contact', 'email']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Person, PersonAdmin)

class RoleAdmin(admin.ModelAdmin):
    """Definition of the Role editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['color']}),
        ('_12M', {'fields': ['actor']}),
        ('_M2M', {'fields': ['gadgets']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Role, RoleAdmin)

class LocationAdmin(admin.ModelAdmin):
    """Definition of the Location editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_M2M', {'fields': ['persons']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['project']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Location, LocationAdmin)

class ScriptAdmin(admin.ModelAdmin):
    """Definition of the Script editor."""
    fieldsets = [
        (None, {'fields': ['workingtitle']}),
        ('_Prop', {'fields': ['abstract', 'description', 'author', 'version', 'copyright',]}),
        ('_12M', {'fields': ['project']}),
        ('_M2M', {'fields': ['persons']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('workingtitle', 'abstract', 'description')
    list_filter = ['project']
    search_fields = ['workingtitle']
    #date_hierarchy = 'pub_date'

admin.site.register(Script, ScriptAdmin)

class SceneAdmin(admin.ModelAdmin):
    """Definition of the Scene editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['order', 'short', 'abstract', 'indentation', 'color', 'duration', 'progress_script', 'progress_pre', 'progress_shot', 'progress_post']}),
        ('_12M', {'fields': ['script', 'set_location']}),
        ('_M2M', {'fields': ['persons', 'gadgets', 'audios', 'sfxs']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('order', 'short', 'name', 'abstract')
    list_filter = ['project', 'script']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Scene, SceneAdmin)

class SceneItemAdmin(admin.ModelAdmin):
    """Definition of the SceneItem editor."""
    fieldsets = [
        ('_Prop', {'fields': ['order', 'type', 'parenthetical', 'text']}),
        ('_12M', {'fields': ['role', 'scene']}),
    ]
    list_display = ('order', 'type', 'role', 'parenthetical', 'text')
    list_filter = ['scene']
    search_fields = ['text']
    #date_hierarchy = 'order'

admin.site.register(SceneItem, SceneItemAdmin)

class A2SInline(admin.TabularInline):
    model = Appointment2Scene
    extra = 1

class AppointmentAdmin(admin.ModelAdmin):
    """Definition of the Appointment editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'project', 'note']}),
        ('_Prop', {'fields': ['time_all', 'duration_all']}),
        ('_12M', {'fields': ['meeting_point']}),
        ('_M2M', {'fields': ['persons', 'gadgets']}),
        #('_M2Mt', {'fields': ['scenes']}),  #JK Error
    ]
    inlines = [A2SInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Appointment, AppointmentAdmin)

