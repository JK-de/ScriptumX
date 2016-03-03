"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
#from datetime import datetime
from django.contrib.auth.models import User

###############################################################################

class Project(models.Model):
    #Props
    name = models.CharField(max_length=30)
    # One to Many
    ###creater = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    #        models.ForeignKey(settings.AUTH_USER_MODEL)
    # Many to Many
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        """Returns a string representation of a Script."""
        return self.name

###############################################################################

class BaseModel(models.Model):
    class Meta:
        # model metadata options go here
        ###abstract = True
        ordering = ['-name']

    #Props
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    #tag_map = models.PositiveIntegerField(default=0x7FFFFFFF)
    marker_map = models.PositiveIntegerField(default=0)

    tag0 = models.BooleanField(default=False, verbose_name='')
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

    # One to Many
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        """Returns a string representation of a Base-Item."""
        return self.name

    def getTag(self, idx):
        if idx == 0:
            return tag0
        if idx == 1:
            return tag1
        if idx == 2:
            return tag2
        if idx == 3:
            return tag3
        if idx == 4:
            return tag4
        if idx == 5:
            return tag5
        if idx == 6:
            return tag6
        if idx == 7:
            return tag7
        if idx == 8:
            return tag8
        if idx == 9:
            return tag9
        if idx == 10:
            return tag10
        if idx == 11:
            return tag11
        return None

###############################################################################

class Note(models.Model):
    #Props
    text = models.CharField(max_length=1000)
    # One to Many
    source = models.ForeignKey(BaseModel, on_delete=models.CASCADE, null=True, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        """Returns a string representation of a Note."""
        return self.name

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
    contact = models.CharField(max_length=1000, blank=True)
    email = models.EmailField(blank=True)
    # Many to Many

###############################################################################

class Role(BaseModel):
    #Props
    color = models.PositiveIntegerField(default=0xFFFFFF)
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
    #Props
    order = models.PositiveIntegerField(default=0)
    variant = models.PositiveIntegerField(default=0)
    indentation = models.PositiveIntegerField(default=0)
    color = models.PositiveIntegerField(default=0)
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
