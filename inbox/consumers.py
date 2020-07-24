import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Thread, ChatMessage
from my_app.rest_serializers import UserExtensionSerializer


class SendMessageConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)

        # self.chat_room = chat_room

    async def websocket_connect(self, event):
        # print('connected', event)

        user = self.scope['user']
        another_user = self.scope['url_route']['kwargs']['username']
        thread_obj = await self.get_thread(user, another_user)
        chat_room = f'chat_{thread_obj.id}'
        self.thread_obj = thread_obj
        self.chat_room = chat_room
        self.user = user
        self.another_user = another_user

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('received', event)
        form_from_front_end = event.get('text', None)
        if form_from_front_end is not None:
            loaded_dict_data = json.loads(form_from_front_end)
            msg = loaded_dict_data.get('message')
            sender = loaded_dict_data.get('username')

            await self.create_new_message(self.user, msg)

            data_to_front = {
                'username': self.user.username,
                'message': msg
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(data_to_front)
                }
            )

    async def chat_message(self, event):

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_new_message(self, me, msg):

        user_to_send_to = User.objects.get(username=self.another_user)

        user_to_send_to_notifications = user_to_send_to.userextension.notifications

        type_of_notifications = type(user_to_send_to_notifications)

        if type_of_notifications == dict:
            identity = 2
        elif type_of_notifications == list:
            identity = user_to_send_to_notifications[-1]['id'] + 1
            print('ID', identity)
            print('THE TYPE AT THIS POINT one is', type(user_to_send_to_notifications))

        new_notification = {
            "id": identity,
            "type": "message",
            "by": UserExtensionSerializer(me.userextension, many=False).data,
            "date_sent": "today"
        }

        if type_of_notifications == dict:
            s = [user_to_send_to_notifications, new_notification]
            user_to_send_to.userextension.notifications = s
            user_to_send_to.userextension.save()

        elif type_of_notifications == list:
            s = user_to_send_to_notifications
            print('Before adding', len(user_to_send_to.userextension.notifications))
            s.append(new_notification)
            user_to_send_to.userextension.notifications = s
            user_to_send_to.userextension.save()
            print('SAVED ANOTHER', len(user_to_send_to.userextension.notifications))
        else:
            pass

        thread_obj = self.thread_obj
        chat = ChatMessage(thread=thread_obj, user=me, message=msg)
        return chat.save()
