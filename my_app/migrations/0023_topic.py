# Generated by Django 3.0.2 on 2020-05-17 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0022_discuzz_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
                ('subtopic', models.CharField(max_length=50)),
            ],
        ),
    ]