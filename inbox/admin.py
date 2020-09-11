from django.contrib import admin
from .models import *


# Register your models here.


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Emoji)
