"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
#from datetime import datetime
#from django.contrib import auth #JK TODO user from django


class UserX(models.Model):
    #Props
    name = models.CharField(max_length=30)
    #Lists

    def __str__(self):
        """Returns a string representation of a User."""
        return self.name



class BaseModel(models.Model):
    #Props
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    tag_map = models.PositiveIntegerField(default=0x7FFFFFFF)
    marker_map = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Returns a string representation of a Base-Item."""
        return self.name

class Note(models.Model):
    #Props
    text = models.CharField(max_length=1000)
    #Link
    source = models.ForeignKey(BaseModel, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        """Returns a string representation of a Note."""
        return self.name

class Gadget(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    #Lists

class Audio(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    #Lists

class SFX(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    #Lists

class Person(BaseModel):
    #Props
    contact = models.CharField(max_length=1000, blank=True)
    email = models.EmailField(blank=True)
    #Lists

class Role(BaseModel):
    #Props
    color = models.PositiveIntegerField(default=0xFFFFFF)
    #Link
    actor = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    #Lists
    gadgets = models.ManyToManyField(Gadget, blank=True)

class Location(BaseModel):
    #Props
    #Lists
    persons = models.ManyToManyField(Person, blank=True)

class Script(models.Model):
    #Props
    workingtitle = models.CharField(max_length=30)
    abstract = models.CharField(max_length=300)
    autor = models.CharField(max_length=300)
    version = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    #Lists
    persons = models.ManyToManyField(Person, blank=True)
    user = models.ManyToManyField(UserX, blank=True)   #JK TODO user from django

    def __str__(self):
            """Returns a string representation of a Script."""
            return self.workingtitle

class Scene(BaseModel):
    #Props
    order = models.PositiveIntegerField(default=0)
    text = models.TextField(blank=True)
    variantmap = models.PositiveIntegerField(default=0)
    intent = models.PositiveIntegerField(default=0)
    color = models.PositiveIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True)
    progress_script = models.PositiveSmallIntegerField(default=0)
    progress_pre = models.PositiveSmallIntegerField(default=0)
    progress_shot = models.PositiveSmallIntegerField(default=0)
    progress_post = models.PositiveSmallIntegerField(default=0)
    #Link
    script = models.ForeignKey(Script, on_delete=models.CASCADE, null=True, blank=True)
    set = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    #Lists
    roles = models.ManyToManyField(Role, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)
    audios = models.ManyToManyField(Audio, blank=True)
    sfxs = models.ManyToManyField(SFX, blank=True)
    #locations = models.ManyToManyField(Location)

class SceneItem(models.Model):
    #Props
    order = models.PositiveIntegerField(default=0)
    parenthetical = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)

    #Lists
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
            """Returns a string representation of a DialogItem."""
            return self.text

class Appointment(BaseModel):
    #Props
    time_all = models.DateTimeField(null=True, blank=True)
    duration_all = models.DurationField(blank=True, null=True)
    #Link
    meeting_point = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    #Lists
    scenes = models.ManyToManyField(Scene,
        through='Appointment2Scene',
        #through_fields=('appointment', 'scene'),
        null=True, blank=True,
        )
    #scenes = models.ManyToManyField(Scene)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)

class Appointment2Scene(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    #Props
    time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)





class Poll(models.Model):
    """A poll object for use in the application views and repository."""
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    #x = models.ForeignKey(Script, null=True, blank=True)

    def total_votes(self):
        """Calculates the total number of votes for this poll."""
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

    def __unicode__(self):
        """Returns a string representation of a poll."""
        return self.text

class Choice(models.Model):
    """A poll choice object for use in the application views and repository."""
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def votes_percentage(self):
        """Calculates the percentage of votes for this choice."""
        total = self.poll.total_votes()
        return self.votes / float(total) * 100 if total > 0 else 0

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.text


