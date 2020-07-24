from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from .models import Thread, ChatMessage

# Create your views here.
from my_app.rest_serializers import UserExtensionSerializer


def chat(request, username):
    another_user = User.objects.get(username=username)
    thread_object = Thread.objects.get_or_new(request.user, another_user)[0]
    chat_messages = ChatMessage.objects.filter(thread=thread_object)
    chat_with = f'chat with {username}'

    user_to_send_to = User.objects.get(username=username)
    user_to_send_to.userextension.friend_requests.add(request.user)
    user_to_send_to.save()

    user_to_send_to_notifications = user_to_send_to.userextension.notifications

    type_of_notifications = type(user_to_send_to_notifications)

    if type_of_notifications == dict:
        identity = 2
    elif type_of_notifications == list:
        if len(user_to_send_to_notifications) == 0:
            identity = 0
        else:
            identity = user_to_send_to_notifications.pop()['id'] + 1

    new_notification = {
        'id': identity,
        'type': 'request',
        'by':   UserExtensionSerializer(request.user.userextension, many=False).data,
        'date_sent': 'today'
    }

    if type_of_notifications == dict:
        s = [user_to_send_to_notifications, new_notification]
        user_to_send_to.userextension.notifications = s
        user_to_send_to.userextension.save()

    elif type_of_notifications == list:
        s = user_to_send_to_notifications
        s.append(new_notification)
        user_to_send_to.userextension.notifications = s
        user_to_send_to.userextension.save()
    else:
        print('NEW TYPE IS: ', type(type_of_notifications))

    context = {
        'other_user': another_user,
        'chat_messages': chat_messages,
        'page': chat_with
    }
    return render(request, 'inbox/chat.html', context)
