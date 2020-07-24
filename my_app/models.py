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


class Friend(models.Model):
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend')


class Languages(models.Model):
    languages = (
        ('java', 'Java'),
        ('javascript', 'Javascript'),
    )
    choices = models.CharField(choices=languages, blank=True, null=True, max_length=30)


class JSONCharField(models.TextField):
    def to_python(self, value):
        if value == "":
            return None
        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass

    def from_db_value(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
            return value


class UserExtension(models.Model):
    sheet = (
        ('prettify', 'default'),
        ('desert', 'desert'),
        ('doxy', 'doxy'),
        ('sons-of-obsidian', 'sons-of-obsidian'),
        ('sunburst', 'sunburst')

    )
    mode = (
        ('light', 'light'),
        ('dark', 'dark')
    )
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    languages = (
        ('Java', 'Java'),
        ('Javascript', 'Javascript'),
        ('C', 'C'),
        ('C#', 'C#'),
        ('C++', 'C++'),
        ('Objective-c', 'Objective-C'),
        ('Php', 'Php'),
        ('Python', 'Python'),
        ('Javascript', 'Javascript'),
        ('Ruby', 'Ruby'),
        ('Perl', 'Perl'),
        ('Clojure', 'Clojure'),
        ('Scala', 'Scala'),
        ('Go', 'Go'),
        ('R*', 'R*'),
        ('Tcl', 'Tcl'),
        ('Lua', 'Lua'),
        ('Bash', 'Bash'),
        ('Visual Basic.NET', 'Visual Basic.NET'),
        ('Haskel', 'Haskel'),
    )
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE, blank=True, null=True)
    style_sheet = models.TextField(null=True, blank=True, default=sheet[1][1], choices=sheet)
    mode_sheet = models.TextField(null=True, blank=True, default=mode[1][0], choices=mode)
    profile_pic = models.ImageField(blank=True,
                                    null=True,
                                    default='/default.png')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='friends')
    friend_requests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='friend_requests')

    location = models.CharField(default='', null=True, blank=True, max_length=100)
    phone_number = models.CharField(default='+254 7 06 522 473', null=True, blank=True, max_length=20)
    gender = models.TextField(default='Not set', blank=True, null=True, choices=gender_choices, max_length=10)
    bio = models.CharField(default='I love discuzz since it is the best discussion platform.',
                           max_length=200, blank=True, null=True)
    programming_languages = MultiSelectField(choices=languages, max_choices=20, blank=True, null=True)

    notifications = jsonfield.JSONField(default=[{"id": 0, "type": "visiting message", "by": "Discuzz"}])

    hobbies = models.CharField(blank=True, null=True, max_length=200)

    status = models.TextField(blank=True, null=True, max_length=200, default='offline')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserExtension.objects.create(user=instance)
        # post_save.connect(UserExtension, sender=User)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userextension.save()


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

    def where(self):
        return self.discussion_code


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
