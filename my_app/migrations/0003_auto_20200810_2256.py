# Generated by Django 3.0.8 on 2020-08-10 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_syntax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friend',
        ),
        migrations.DeleteModel(
            name='Languages',
        ),
        migrations.DeleteModel(
            name='Syntax',
        ),
        migrations.RemoveField(
            model_name='userextension',
            name='friend_requests',
        ),
        migrations.RemoveField(
            model_name='userextension',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='userextension',
            name='user',
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
        migrations.DeleteModel(
            name='UserExtension',
        ),
    ]
