# Generated by Django 3.0.8 on 2020-08-10 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_auto_20200810_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syntax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
