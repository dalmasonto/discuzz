from django.contrib import admin
from .models import *


# Register your models here.


class CreateAdmin(admin.ModelAdmin):
    list_display = ('topic', 'admin', 'paymentMode', 'paymentCode', 'subtopic', 'description', 'question',
                    'discussionCode', 'createTime')


class DiscuzzAdmin(admin.ModelAdmin):
    list_display = ('discussion_code', 'reply', 'username', 'reply_time')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'subtopic')


admin.site.register(Create, CreateAdmin)
admin.site.register(Discuzz, DiscuzzAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(SendEmail)
