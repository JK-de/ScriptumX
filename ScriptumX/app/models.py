"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
#from datetime import datetime
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from django.conf import settings
from django.contrib.auth import get_user_model

###############################################################################

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):
    #Props
    name = models.CharField(max_length=30)
    # One to Many
    ###creater = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    #        models.ForeignKey(settings.AUTH_USER_MODEL)
    # Many to Many
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        #on_delete=models.SET(get_sentinel_user), 
        blank=True)

    def __str__(self):
        """Returns a string representation of a Script."""
        return self.name

###############################################################################

class Note(models.Model):
    #Props
    text = models.TextField(blank=True)
    # One to Many
    #source = models.ForeignKey(BaseModel, 
    #    on_delete=models.CASCADE,
    #    related_name="notes",
    #    related_query_name="note",
    #    null=True, 
    #    blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        """Returns a string representation of a Note."""
        return self.text

###############################################################################

class BaseModel(models.Model):
    class Meta:
        # model metadata options go here
        #abstract = True
        ordering = ['name']

    #Props
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    #tag_map = models.PositiveIntegerField(default=0x7FFFFFFF)
    marker_map = models.PositiveIntegerField(default=0)

    tag1 = models.BooleanField(default=False, verbose_name='')
    tag2 = models.BooleanField(default=False, verbose_name='')
    tag3 = models.BooleanField(default=False, verbose_name='')
    tag4 = models.BooleanField(default=False, verbose_name='')
    tag5 = models.BooleanField(default=False, verbose_name='')
    tag6 = models.BooleanField(default=False, verbose_name='')
    tag7 = models.BooleanField(default=False, verbose_name='')
    tag8 = models.BooleanField(default=False, verbose_name='')
    tag9 = models.BooleanField(default=False, verbose_name='')
    tag10 = models.BooleanField(default=False, verbose_name='')
    tag11 = models.BooleanField(default=False, verbose_name='')
    tag12 = models.BooleanField(default=False, verbose_name='')

    # One to Many
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)
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

###############################################################################

class Gadget(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class Audio(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class SFX(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    # Many to Many

###############################################################################

class Person(BaseModel):
    #Props
    contact = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    # Many to Many

###############################################################################

class Role(BaseModel):
    #Props
    color = RGBColorField()
    # One to Many
    actor = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    # Many to Many
    gadgets = models.ManyToManyField(Gadget, blank=True)

###############################################################################

class Location(BaseModel):
    #Props
    # Many to Many
    persons = models.ManyToManyField(Person, blank=True)

###############################################################################

class Script(models.Model):
    #Props
    workingtitle = models.CharField(max_length=30)
    abstract = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=300, blank=True)
    version = models.CharField(max_length=30, blank=True)
    copyright = models.CharField(max_length=300, blank=True)
    # One to Many
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)
    # Many to Many
    persons = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        """Returns a string representation of a Script."""
        return self.workingtitle

###############################################################################

class Scene(BaseModel):
    class Meta:
        # model metadata options go here
        ordering = ['order']

    #Props
    order = models.PositiveIntegerField(default=0)
    variant = models.PositiveIntegerField(default=0)
    indentation = models.PositiveIntegerField(default=0)
    color = RGBColorField()
    duration = models.DurationField(null=True, blank=True)
    progress_script = models.PositiveSmallIntegerField(default=0)
    progress_pre = models.PositiveSmallIntegerField(default=0)
    progress_shot = models.PositiveSmallIntegerField(default=0)
    progress_post = models.PositiveSmallIntegerField(default=0)
    # One to Many
    ###project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, null=True, blank=True)
    set_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    # Many to Many
    #roles = models.ManyToManyField(Role, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)
    audios = models.ManyToManyField(Audio, blank=True)
    sfxs = models.ManyToManyField(SFX, blank=True)
    #locations = models.ManyToManyField(Location)

###############################################################################

class SceneItem(models.Model):
    class Meta:
        # model metadata options go here
        ordering = ['order']

    #Props
    order = models.PositiveIntegerField(default=0)
    parenthetical = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)

    # Many to Many
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        """Returns a string representation of a DialogItem."""
        return self.text

###############################################################################

class Appointment(BaseModel):
    class Meta:
        # model metadata options go here
        ordering = ['time_all']

    #Props
    time_all = models.DateTimeField(null=True, blank=True)
    duration_all = models.DurationField(blank=True, null=True)
    # One to Many
    meeting_point = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    # Many to Many
    scenes = models.ManyToManyField(Scene,
        through='Appointment2Scene',
        #through_fields=('appointment', 'scene'),
        blank=True,
        )
    #scenes = models.ManyToManyField(Scene)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)

class Appointment2Scene(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, null=True, blank=True, on_delete=models.CASCADE)
    #Props
    time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

###############################################################################
