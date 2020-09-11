import jsonfield
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


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

    # notifications = jsonfield.JSONField(default=[{"id": 0, "type": "visiting message", "by": "Discuzz"}])
    # notifications = models.JSONField(default=[()], blank=True, null=True)

    hobbies = models.CharField(blank=True, null=True, max_length=200)

    status = models.TextField(blank=True, null=True, max_length=200, default='offline')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserExtension.objects.create(user=instance)
            instance.userextension.save()

            # post_save.connect(UserExtension, sender=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        UserExtension.objects.get_or_create(user=instance)
        instance.userextension.save()


class Notification(models.Model):
    kind = models.TextField(default='welcome', blank=True, null=True)
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification', blank=True, null=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', blank=True, null=True)
    where = models.TextField(blank=True, null=True)
    question_code = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    when = models.DateTimeField(auto_now_add=True)
