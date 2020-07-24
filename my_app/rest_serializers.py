from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import serializers

from my_app.models import UserExtension

from .models import Discuzz, Create


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserExtensionSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserExtension
        fields = ['user', 'style_sheet', 'mode_sheet',
                  'profile_pic', 'location',
                  'phone_number', 'gender', 'bio', 'hobbies', 'status'
                  ]

        # def create(self, validated_data):
        #     user_data = validated_data.pop('user')
        #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        #     user, user_extension = UserExtension.objects.update_or_create(user=user,)


class DiscuzzReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Discuzz
        fields = '__all__'


class DiscuzzQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Create
        fields = '__all__'
