# Generated by Django 3.0.2 on 2020-01-24 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_auto_20200119_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField()),
                ('text', models.CharField(max_length=200)),
            ],
        ),
    ]
