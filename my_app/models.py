from django.db import models


# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'


class Add(models.Model):
    added_date = models.DateTimeField()
    text = models.CharField(max_length=200)


class UserSignup(models.Model):
    username = models.CharField(max_length=100)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.IntegerField()
    password = models.CharField(max_length=300)
