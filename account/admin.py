from django.contrib import admin

# Register your models here.
from .models import UserExtension, Notification

admin.site.register(UserExtension)
admin.site.register(Notification)
