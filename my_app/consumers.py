import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from my_app.models import SendEmail


class SendEmailConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    async def websocket_connect(self, event):
        print('connected', event)

        chat_room = 'emails'
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })
        print(self.scope['user'])

    async def websocket_receive(self, event):
        print('received', event)
        form_from_front_end = event.get('text', None)
        loaded_dict_data = json.loads(form_from_front_end)
        email = loaded_dict_data.get('email')
        msg = loaded_dict_data.get('message')

        await self.create_new_email(email, msg)
        print(email, msg)
        data_to_front = {
            'email': email,
            'message': msg
        }
        new_data = {
            'type': 'websocket.send',
            'text': json.dumps(data_to_front)
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'email_chat',
                'text': json.dumps(data_to_front)
            }
        )

    async def email_chat(self, event):
        # print('MESSAGE', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def create_new_email(self, email, msg):
        now = timezone.now()
        chat = SendEmail(email=email, update=msg, updateTime=now)
        # chat.save()
        # print('This is the msg', chat)
        return chat.save()
