"""
Customizations for the Django administration interface.
"""

from django.contrib import admin
from app.models import *

#class ChoiceInline(admin.TabularInline):
#    """Choice objects can be edited inline in the Poll editor."""
#    model = Choice
#    extra = 3

#class PollAdmin(admin.ModelAdmin):
#    """Definition of the Poll editor."""
#    fieldsets = [
#        (None, {'fields': ['text']}),
#        ('Date information', {'fields': ['pub_date']}),
#    ]
#    inlines = [ChoiceInline]
#    list_display = ('text', 'pub_date')
#    list_filter = ['pub_date']
#    search_fields = ['text']
#    date_hierarchy = 'pub_date'

#admin.site.register(Poll, PollAdmin)

class ScriptAdmin(admin.ModelAdmin):
    """Definition of the Script editor."""
    fieldsets = [
        (None, {'fields': ['workingtitle']}),
        ('_Base', {'fields': ['description']}),
        ('_M2M', {'fields': ['persons']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('workingtitle', 'description')
    list_filter = ['workingtitle']
    search_fields = ['workingtitle']
    #date_hierarchy = 'pub_date'

admin.site.register(Script, ScriptAdmin)

class SceneAdmin(admin.ModelAdmin):
    """Definition of the Scene editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag_map', 'marker_map']}),
        ('_Prop', {'fields': ['order', 'text', 'variantmap', 'intent', 'color', 'duration', 'progress_script', 'progress_pre', 'progress_shot', 'progress_post']}),
        ('_12M', {'fields': ['script', 'set']}),
        ('_M2M', {'fields': ['roles', 'persons', 'gadgets', 'audios', 'sfxs']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Scene, SceneAdmin)

class GadgetAdmin(admin.ModelAdmin):
    """Definition of the Gadget editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9',  'tag10',  'tag11', 'tag12', 'marker_map']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Gadget, GadgetAdmin)

class AudioAdmin(admin.ModelAdmin):
    """Definition of the Audio editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'marker_map']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Audio, AudioAdmin)

class SfxAdmin(admin.ModelAdmin):
    """Definition of the SFX editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'marker_map']}),
        ('_Prop', {'fields': ['progress']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(SFX, SfxAdmin)

class PersonAdmin(admin.ModelAdmin):
    """Definition of the Person editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'marker_map']}),
        ('_Prop', {'fields': ['contact', 'email']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Person, PersonAdmin)

class RoleAdmin(admin.ModelAdmin):
    """Definition of the Role editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', ]}),
        ('_Prop', {'fields': ['color']}),
        ('_12M', {'fields': ['actor']}),
        ('_M2M', {'fields': ['gadgets']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Role, RoleAdmin)

class LocationAdmin(admin.ModelAdmin):
    """Definition of the Location editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'marker_map']}),
        ('_M2M', {'fields': ['persons']}),
    ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']
    #date_hierarchy = 'pub_date'

admin.site.register(Location, LocationAdmin)

class A2SInline(admin.TabularInline):
    model = Appointment2Scene
    extra = 1

class AppointmentAdmin(admin.ModelAdmin):
    """Definition of the Appointment editor."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('_Base', {'fields': ['description', 'marker_map']}),
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

class SceneItemAdmin(admin.ModelAdmin):
    """Definition of the SceneItem editor."""
    fieldsets = [
        ('_Prop', {'fields': ['order', 'parenthetical', 'text']}),
        ('_12M', {'fields': ['role', 'scene']}),
    ]
    list_display = ('order', 'text')
    list_filter = ['order']
    search_fields = ['text']
    #date_hierarchy = 'order'

admin.site.register(SceneItem, SceneItemAdmin)

class NoteAdmin(admin.ModelAdmin):
    """Definition of the Note editor."""
    fieldsets = [
        ('_Prop', {'fields': ['text']}),
        ('_12M', {'fields': ['project']}),
    ]
    list_display = ('text', 'project')
    list_filter = ['text']
    search_fields = ['text']

admin.site.register(Note, NoteAdmin)

