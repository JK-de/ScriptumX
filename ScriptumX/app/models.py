"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
#from datetime import datetime


class BaseModel(models.Model):
    #Props
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    tag_map = models.PositiveIntegerField(default=0x7FFFFFFF)
    marker_map = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.name

class Note(models.Model):
    #Props
    text = models.CharField(max_length=1000)
    #Link
    source = models.ForeignKey(BaseModel, on_delete=models.CASCADE, null=True, blank=False)

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.name

class Gadget(BaseModel):
    #Props
    progress = models.PositiveSmallIntegerField(default=0)
    #Lists

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.name

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
    set = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    #Lists
    roles = models.ManyToManyField(Role, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    gadgets = models.ManyToManyField(Gadget, blank=True)
    audios = models.ManyToManyField(Audio, blank=True)
    sfxs = models.ManyToManyField(SFX, blank=True)
    #locations = models.ManyToManyField(Location)

class Script(models.Model):
    #Props
    workingtitle = models.CharField(max_length=30)
    abstract = models.CharField(max_length=300)
    autor = models.CharField(max_length=300)
    version = models.CharField(max_length=300)
    description = models.CharField(max_length=300, blank=True)
    #Lists
    scenes = models.ManyToManyField(Scene, blank=True)
    persons = models.ManyToManyField(Person, blank=True)

    def __unicode__(self):
            """Returns a string representation of a choice."""
            return self.workingtitle

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

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.name

class Appointment2Scene(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    #Props
    time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)


class User(models.Model):
    #Props
    name = models.CharField(max_length=30)
    #Lists
    scripts = models.ManyToManyField(Script)

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.name




class Poll(models.Model):
    """A poll object for use in the application views and repository."""
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    x = models.ForeignKey(Script)

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


