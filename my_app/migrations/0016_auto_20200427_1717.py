# Generated by Django 3.0.2 on 2020-04-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0015_sendemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discuzz',
            name='reply',
            field=models.CharField(max_length=6000),
        ),
    ]
