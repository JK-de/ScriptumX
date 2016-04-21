"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
#from datetime import datetime
from django.contrib.auth.models import User
from colorful.fields import RGBColorField   # replaced by colorfield
from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime

from .tags import *

###############################################################################

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):
    #Props
    name = models.CharField(max_length=50)
    # One to Many
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="project_owned",)
    # Many to Many
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="project_user", blank=True)
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="project_guest", blank=True)

    def __str__(self):
        """Returns a string representation of a Script."""
        return self.name

###############################################################################

class Note(models.Model):
    #Props
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # One to Many
    author = models.ForeignKey(User, null=True)
    #source = models.ForeignKey(BaseModel, 
    #    on_delete=models.CASCADE,
    #    related_name="notes",
    #    related_query_name="note",
    #    null=True, 
    #    blank=False)
    project = models.ForeignKey(Project)

    def __init__(self, *args, **kwargs):
        super(Note, self).__init__(*args, **kwargs)
        #self.project = project
        self.created = datetime.now()

    def __str__(self):
        """Returns a string representation of a Note."""
        return self.text

###############################################################################

class BaseModel(models.Model):
    class Meta:
        # model metadata options go here
        abstract = True
        ordering = ['name']

    #Props
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    tag1 = models.BooleanField(default=False, verbose_name='a')
    tag2 = models.BooleanField(default=False, verbose_name='b')
    tag3 = models.BooleanField(default=False, verbose_name='c')
    tag4 = models.BooleanField(default=False, verbose_name='d')
    tag5 = models.BooleanField(default=False, verbose_name='e')
    tag6 = models.BooleanField(default=False, verbose_name='')
    tag7 = models.BooleanField(default=False, verbose_name='')
    tag8 = models.BooleanField(default=False, verbose_name='')
    tag9 = models.BooleanField(default=False, verbose_name='')
    tag10 = models.BooleanField(default=False, verbose_name='')
    tag11 = models.BooleanField(default=False, verbose_name='')
    tag12 = models.BooleanField(default=False, verbose_name='')

    # One to Many
    project = models.ForeignKey(Project)   # for internal relations only
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        """Returns a string representation of a Base-Item."""
        return self.name


    def getTag(self, idx):
        if idx == 1:
            return self.tag1
        if idx == 2:
            return self.tag2
        if idx == 3:
            return self.tag3
        if idx == 4:
            return self.tag4
        if idx == 5:
            return self.tag5
        if idx == 6:
            return self.tag6
        if idx == 7:
            return self.tag7
        if idx == 8:
            return self.tag8
        if idx == 9:
            return self.tag9
        if idx == 10:
            return self.tag10
        if idx == 11:
            return self.tag11
        if idx == 12:
            return self.tag12
        return None


    def setTag(self, idx, value):
        if idx == 1:
            self.tag1 = value
        if idx == 2:
            self.tag2 = value
        if idx == 3:
            self.tag3 = value
        if idx == 4:
            self.tag4 = value
        if idx == 5:
            self.tag5 = value
        if idx == 6:
            self.tag6 = value
        if idx == 7:
            self.tag7 = value
        if idx == 8:
            self.tag8 = value
        if idx == 9:
            self.tag9 = value
        if idx == 10:
            self.tag10 = value
        if idx == 11:
            self.tag11 = value
        if idx == 12:
            self.tag12 = value


    def getTagList(self):
        return (
            self.tag1 ,
            self.tag2 ,
            self.tag3 ,
            self.tag4 ,
            self.tag5 ,
            self.tag6 ,
            self.tag7 ,
            self.tag8 ,
            self.tag9 ,
            self.tag10,
            self.tag11,
            self.tag12,
            )


    def setAllTags(self, value):
        #self.project = project
        self.tag1 = value
        self.tag2 = value
        self.tag3 = value
        self.tag4 = value
        self.tag5 = value
        self.tag6 = value
        self.tag7 = value
        self.tag8 = value
        self.tag9 = value
        self.tag10 = value
        self.tag11 = value
        self.tag12 = value

    @property
    def active_tag_images(self):
        list = []

        for tag in all_tag_list[self.group_id]:
            if self.getTag(tag['idx']):
                list.append(tag['img'])

        return list

###############################################################################

class Gadget(BaseModel):
    group_id = 'gadget'
    #Props
    pervasive = models.BooleanField(default=False)
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class Audio(BaseModel):
    group_id = 'audio'
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class SFX(BaseModel):
    group_id = 'sfx'
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class Person(BaseModel):
    group_id = 'person'
    #Props
    pervasive = models.BooleanField(default=False)
    contact = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    # Many to Many

###############################################################################

class Role(BaseModel):
    group_id = 'role'
    #Props
    color = ColorField(default='#FFFFFF')
    # One to Many
    actor = models.ForeignKey(Person, null=True, blank=True)
    # Many to Many
    gadgets = models.ManyToManyField(Gadget, blank=True)

###############################################################################

class Location(BaseModel):
    group_id = 'location'
    #Props
    # Many to Many
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)

###############################################################################

class Script(models.Model):
    #Props
    name = models.CharField(max_length=50)
    abstract = models.TextField(blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=300, blank=True)
    version = models.CharField(max_length=50, blank=True)
    copyright = models.CharField(max_length=300, blank=True)
    # One to Many
    project = models.ForeignKey(Project)   # for internal relations only
    # Many to Many
    persons = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        """Returns a string representation of a Script."""
        return self.name

###############################################################################

class Scene(BaseModel):
    group_id = 'scene'
    class Meta:
        # model metadata options go here
        ordering = ['order']

    #Props
    order = models.PositiveIntegerField(default=0)
    short = models.CharField(max_length=5, blank=True, default='')
    abstract = models.TextField(blank=True)
    indentation = models.PositiveIntegerField(default=0)
    color = ColorField(default='#FFFFFF', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    progress_script = models.PositiveSmallIntegerField(default=0)
    progress_pre = models.PositiveSmallIntegerField(default=0)
    progress_shot = models.PositiveSmallIntegerField(default=0)
    progress_post = models.PositiveSmallIntegerField(default=0)
    # One to Many
    script = models.ForeignKey(Script)   # for internal relations only
    set_location = models.ForeignKey(Location, null=True, blank=True)
    # Many to Many
    #roles = models.ManyToManyField(Role, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)
    audios = models.ManyToManyField(Audio, blank=True)
    sfxs = models.ManyToManyField(SFX, blank=True)

    def __init__(self, *args, **kwargs):
        #self.project = project
        self.setAllTags(True)   #JKJKJK
        super(Scene, self).__init__(*args, **kwargs)

###############################################################################

class SceneItem(models.Model):
    class Meta:
        # model metadata options go here
        ordering = ['order']

    #Props
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=1, blank=True, default='')
    parenthetical = models.CharField(max_length=100, blank=True, default='')
    text = models.TextField(blank=True)

    # Many to Many
    role = models.ForeignKey(Role, null=True, blank=True)
    scene = models.ForeignKey(Scene, null=True, blank=True)   # for internal relations only
    
    def __str__(self):
        """Returns a string representation of a DialogItem."""
        return self.text

###############################################################################

class Appointment(BaseModel):
    group_id = 'appointment'
    class Meta:
        # model metadata options go here
        ordering = ['time_all']

    #Props
    time_all = models.DateTimeField(null=True, blank=True)
    duration_all = models.DurationField(blank=True, null=True)
    # One to Many
    meeting_point = models.ForeignKey(Location, null=True, blank=True)
    # Many to Many
    scenes = models.ManyToManyField(Scene,
        through='Appointment2Scene',
        #through_fields=('appointment', 'scene'),
        blank=True,
        )
    #scenes = models.ManyToManyField(Scene)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)

class Appointment2Scene(models.Model):   # for internal relations only
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene)
    #Props
    time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

###############################################################################
