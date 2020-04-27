from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


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
    reply = models.CharField(max_length=2000)
    username = models.CharField(max_length=50)
    reply_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.discussion_code


class SendEmail(models.Model):
    email = models.CharField(max_length=50)
    update = models.CharField(max_length=2000)
    updateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
