import asyncio
import json
from datetime import datetime

from threading import Timer

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Thread, ChatMessage

from my_app.rest_serializers import chatMessageSerializer


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
        print(self.thread_obj)
        self.chat_room = chat_room
        self.user = user
        self.another_user = another_user
        print(self.another_user)

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
            kind = loaded_dict_data.get('type')
            if kind == 'online':

                await self.set_online_status()

                data_to_front = {
                    'type': 'online',
                    'online': True,
                    'username': self.user.username
                }

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(data_to_front)
                    }
                )
                return
            elif kind == 'message':
                msg = loaded_dict_data.get('message')
                sender = loaded_dict_data.get('username')

                msgs = await self.create_new_message(self.user, msg)
                msg_serializer = chatMessageSerializer(msgs, many=False)
                data_to_front = {
                    'type': 'message',
                    'messageData': msg_serializer.data,
                    'username': self.user.username
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
        await self.set_offline_status()

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def set_online_status(self):
        thread_obj = self.thread_obj

        chat_messages = ChatMessage.objects.filter(thread=thread_obj)
        if thread_obj.first == self.user:
            thread_obj.first_online_state = True
            for msg in chat_messages:
                msg.read_by.add(self.user)
                msg.save()
        else:
            thread_obj.second_online_state = True
            for msg in chat_messages:
                msg.read_by.add(self.user)
                msg.save()

        thread_obj.updated = timezone.now()
        thread_obj.save()

        return thread_obj

    @database_sync_to_async
    def set_offline_status(self):
        thread_obj = self.thread_obj
        if thread_obj.first == self.user:
            thread_obj.first_online_state = False
        else:
            thread_obj.second_online_state = False

        thread_obj.updated = timezone.now()
        thread_obj.save()

        return thread_obj

    @database_sync_to_async
    def create_new_message(self, me, msg):
        thread_obj = self.thread_obj
        chat = ChatMessage(thread=thread_obj, user=me, message=msg)
        chat.save()

        other_user = User.objects.get(username=self.another_user)
        first = thread_obj.first
        second = thread_obj.second

        if first == self.user:
            if thread_obj.first_online_state:
                chat.read_by.add(self.user)

            elif thread_obj.second_online_state:
                chat.read_by.add(other_user)
            # return
        else:
            if thread_obj.second_online_state:
                chat.read_by.add(other_user)
            elif thread_obj.first_online_state:
                chat.read_by.add(self.user)

        thread_obj.updated = timezone.now()
        thread_obj.save()
        chat.save()

        return chat


class SendNotificationsConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    async def websocket_connect(self, event):

        # print(self.scope)

        await self.send({
            'type': 'websocket.accept'
        })

        timer__ = Timer(0.5, self.get_notifications)
        timer__.start()

    async def websocket_receive(self, event):
        print('received', event)
        text = await self.get_notifications()
        await self.send(
            {
                'type': 'websocket.send',
                'text': text
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_notifications(self):
        return 'Successfully received'


