from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.utils.dateformat import format
from psycopg2._psycopg import Date

from rest_framework import serializers

from .models import Discuzz, Create, Comment
from account.models import UserExtension, Notification

from inbox.models import ChatMessage, Thread, Emoji


class UserExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtension
        fields = ['style_sheet', 'mode_sheet',
                  'profile_pic', 'location',
                  'phone_number', 'gender', 'bio', 'hobbies', 'status'
                  ]


class UserSerializer(serializers.ModelSerializer):
    userextension = UserExtensionSerializer(many=False, required=True)

    create_set = 'DiscuzzQuestionSerializer(many=True)'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'userextension', 'create_set']

    # def get_create_set(self, obj):
    #     return 'something'


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer(many=False)
    # commented_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    commented_on = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['commented_to', 'commented_by', 'comment', 'commented_on', 'status']

    def get_commented_on(self, obj):
        time = timesince(obj.commented_on)
        return time


class DiscuzzReplySerializer(serializers.ModelSerializer):
    username = UserSerializer(many=False, read_only=True)
    comment_set = CommentSerializer(many=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    # reply_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    reply_time = serializers.SerializerMethodField()

    class Meta:
        model = Discuzz
        fields = ['id',
                  'discussion_code',
                  'reply',
                  'username',
                  'likes',
                  'dislikes',
                  'comment_set',
                  'reply_time',
                  'comments_count',
                  ]

    def get_likes(self, obj):
        return obj.likes.all().count()

    def get_dislikes(self, obj):
        return obj.dislikes.all().count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_reply_time(self, obj):
        time = timesince(obj.reply_time)
        return time


class DiscuzzQuestionSerializer(serializers.ModelSerializer):
    discuzz_set = DiscuzzReplySerializer(many=True)
    admin = UserSerializer(many=False)
    replies_count = serializers.SerializerMethodField()
    # total_comments_count = serializers.SerializerMethodField()
    # createTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    createTime = serializers.SerializerMethodField()

    class Meta:
        model = Create
        fields = ['admin', 'paymentMode', 'paymentCode',
                  'discussionCode', 'topic', 'subtopic',
                  'description', 'question', 'createTime',
                  'discuzz_set', 'replies_count',

                  ]

    def get_replies_count(self, obj):
        return obj.discuzz_set.count()

    def get_createTime(self, obj):
        time = timesince(obj.createTime)
        return time


class NotificationSerializer(serializers.ModelSerializer):
    by = UserSerializer(many=False, required=True)
    to = UserSerializer(many=False, required=True)

    class Meta:
        model = Notification
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    first = UserSerializer(many=False)
    second = UserSerializer(many=False)
    chatmessage_set = 'chatMessageSerializer(many=True)'
    chatmessage_set_count = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['first', 'second', 'updated', 'timestamp', 'chatmessage_set', 'chatmessage_set_count']

    def get_chatmessage_set_count(self, obj):
        return obj.chatmessage_set.count()

    def get_updated(self, obj):
        c = []
        return format(obj.updated, 'N j, Y, P')


class chatMessageSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False)

    class Meta:
        model = ChatMessage
        fields = ['thread', 'user', 'message', 'timestamp']


class EmojiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emoji
        fields = ['id', 'emoji', 'name']