import json

# from django.contrib.postgres.fields import JSONField
import jsonfield
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField


class Create(models.Model):
    choices = (
        ('visible', 'visible'),
        ('hidden', 'hidden')
    )

    topic = models.CharField(max_length=50)
    admin = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)
    paymentMode = models.CharField(max_length=20, null=True, blank=True)
    paymentCode = models.CharField(max_length=20)
    subtopic = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    question = models.CharField(max_length=1000)
    discussionCode = models.CharField(max_length=100, default='100NO00DISCUSSION001yet11')
    createTime = models.DateTimeField(auto_now_add=True)

    status = models.TextField(choices=choices, default=choices[0][1], blank=True, null=True)

    def __str__(self):
        return self.topic


class Discuzz(models.Model):
    choices = (
        ('visible', 'visible'),
        ('hidden', 'hidden')
    )

    discussion_code = models.ForeignKey(Create, default=None, on_delete=models.SET_NULL, blank=True, null=True)
    reply = models.TextField(max_length=6000)
    username = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)

    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    comments = models.ManyToManyField(User, related_name='comments', blank=True)

    status = models.TextField(choices=choices, default=choices[0][1], blank=True, null=True)

    reply_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.discussion_code.discussionCode


class Comment(models.Model):
    choices = (
        ('visible', 'visible'),
        ('hidden', 'hidden')
    )

    commented_to = models.ForeignKey(Discuzz, default=None, on_delete=models.CASCADE, blank=True, null=True)
    commented_by = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=500)
    commented_on = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=choices, default=choices[0][1], blank=True, null=True)


class SendEmail(models.Model):
    choices = (
        ('unread', 'unread'),
        ('read', 'read')
    )
    state = (
        ('reply', 'reply'),
        ('replied', 'replied')
    )
    email = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null=True)
    update = models.CharField(max_length=2000)
    updateTime = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=choices, default=choices[0][1], blank=True)
    state = models.TextField(choices=state, default=state[0][1], blank=True)

    def __str__(self):
        return self.email.email


class Topic(models.Model):
    choices = (
        ('visible', 'visible'),
        ('hidden', 'hidden')
    )

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.CharField(max_length=50)
    subtopic = models.CharField(max_length=50)
    status = models.TextField(choices=choices, default=choices[0][1], blank=True, null=True)

    def __str__(self):
        return self.topic


class Syntax(models.Model):
    topic = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.topic
