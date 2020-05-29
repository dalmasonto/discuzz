from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User

# Create your models here.
from django.urls import reverse


class Create(models.Model):
    topic = models.CharField(max_length=50)
    admin = models.CharField(max_length=20)
    paymentMode = models.CharField(max_length=20)
    paymentCode = models.CharField(max_length=20)
    subtopic = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    question = models.CharField(max_length=1000)
    discussionCode = models.CharField(max_length=100, default='100NO00DISCUSSION001yet11')
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    def where(self):
        return self.discussion_code


class Discuzz(models.Model):
    discussion_code = models.CharField(max_length=100, default='100NO00DISCUSSION001yet11')
    reply = models.TextField(max_length=6000)
    username = models.CharField(max_length=50)

    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    comments = models.ManyToManyField(User, related_name='comments', blank=True)

    reply_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.discussion_code

    # def get_absolute_url(self):
    #     return reverse("discuzz:discuzz", kwargs={"discussion_details": self.discussion_code})


class Comment(models.Model):
    commented_to = models.ForeignKey(Discuzz, default=None, on_delete=models.SET_NULL, blank=True, null=True)
    commented_by = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=500)
    commented_on = models.DateTimeField(auto_now_add=True)


class SendEmail(models.Model):
    email = models.CharField(max_length=50)
    update = models.CharField(max_length=2000)
    updateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Topic(models.Model):
    topic = models.CharField(max_length=50)
    subtopic = models.CharField(max_length=50)

    def __str__(self):
        return self.topic
