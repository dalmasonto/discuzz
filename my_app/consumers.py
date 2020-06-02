import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import SendEmail, Discuzz, Comment


class SendEmailConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)

        chat_room = 'emails'
        self.chat_room = chat_room

    async def websocket_connect(self, event):
        # print('connected', event)

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })
        # print(self.scope['user'])

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


class SendReplyConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        # print('THE SCOPE HAS THE FOLLOWING INFORMATION', scope)
        chat_room = scope['url_route']['kwargs']['discussion_Code']

        discussion_code = chat_room
        user = scope['user']
        reply_time = timezone.now()

        self.chat_room = chat_room
        self.discussion_code = discussion_code
        self.user = user
        self.reply_time = reply_time
        # print('START', self.reply_time)

    async def websocket_connect(self, event):
        # print('connected', event)

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })
        # print(self)

    async def websocket_receive(self, event):
        # print('received', event)
        form_from_front_end = event.get('text', None)
        loaded_dict_data = json.loads(form_from_front_end)
        # print('THE LOADED DICT DATA', loaded_dict_data)
        type_ = loaded_dict_data.get('type')
        # print('THE TYPE IS: ', type_)

        if type_ == 'reply':
            reply = loaded_dict_data.get('reply')

            await self.create_new_reply(reply)

            new_rep = await self.get_the_new_reply(reply)
            # print('THE NEW REP IS: ', new_rep.reply)

            data_to_front = {
                'id': new_rep.id,
                'username': self.user.username,
                'reply': new_rep.reply,
                'likes': 0,
                'dislikes': 0,
                'comments': 0,
                'type': 'reply'
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'reply_chat',
                    'text': json.dumps(data_to_front)
                }
            )

        elif type_ == 'comment':
            comment = loaded_dict_data.get('comment')
            id_ = loaded_dict_data.get('id')

            await self.create_new_comment(comment, id_)

            data_to_front = {
                'id': id_,
                'username': self.user.username,
                'comment': comment,
                'type': 'comment'
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'comment_chat',
                    'text': json.dumps(data_to_front)
                }
            )

        elif type_ == 'like':
            id_ = loaded_dict_data.get('id')
            print(id_)

            await self.create_like(id_)
            likes = await self.get_reply_likes(id_)
            dislikes = await self.get_reply_dislikes(id_)

            data_to_front = {
                'id': id_,
                'likes': likes,
                'dislikes': dislikes,
                'type': 'like'
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'like_chat',
                    'text': json.dumps(data_to_front)
                }
            )

        elif type_ == 'dislike':
            comment = loaded_dict_data.get('comment')
            id_ = loaded_dict_data.get('id')

            await self.create_dislike(id_)
            dislikes = await self.get_reply_dislikes(id_)
            likes = await self.get_reply_likes(id_)

            data_to_front = {
                'id': id_,
                'dislikes': dislikes,
                'likes': likes,
                'type': 'dislike'
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'dislike_chat',
                    'text': json.dumps(data_to_front)
                }
            )

    async def reply_chat(self, event):
        print('MESSAGE REPLY', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def comment_chat(self, event):
        print('MESSAGE COMMENT', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def like_chat(self, event):
        print('MESSAGE LIKE', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def dislike_chat(self, event):
        print('MESSAGE DISLIKE', event)

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def create_new_reply(self, reply):
        now = timezone.now()
        reply = Discuzz(discussion_code=self.discussion_code, reply=reply, username=self.user,
                        reply_time=now)
        return reply.save()

    @database_sync_to_async
    def create_new_comment(self, comment, id_):
        now = timezone.now()
        query_id = Discuzz.objects.get(id=id_)
        return Comment.objects.create(commented_to=query_id, commented_by=self.user, comment=comment, commented_on=now)

    @database_sync_to_async
    def create_like(self, id_):

        reply = Discuzz.objects.get(id=id_)
        user = self.user
        if reply.dislikes.filter(username=user).exists():
            reply.likes.add(user)
            reply.dislikes.remove(user)

        elif reply.likes.filter(username=user).exists():
            reply.likes.remove(user)
        else:
            reply.likes.add(user)

    @database_sync_to_async
    def create_dislike(self, id_):
        reply = Discuzz.objects.get(id=id_)
        user = self.user
        if reply.likes.filter(username=user).exists():
            reply.dislikes.add(user)
            reply.likes.remove(user)
        elif reply.dislikes.filter(username=user).exists():
            reply.dislikes.remove(user)

        else:
            reply.dislikes.add(user)

    @database_sync_to_async
    def get_the_new_reply(self, reply):
        # print('AFTER', self.reply_time)
        the_new_reply = Discuzz.objects.filter(reply=reply)
        a_rep = the_new_reply[len(the_new_reply) - 1]
        # print('The reply from the database is: ', the_new_reply)

        return a_rep

    @database_sync_to_async
    def get_reply_likes(self, reply_id):
        the_reply = Discuzz.objects.get(id=reply_id)
        reply_likes = the_reply.likes.count()

        return reply_likes

    @database_sync_to_async
    def get_reply_dislikes(self, reply_id):
        the_reply = Discuzz.objects.get(id=reply_id)
        reply_dislikes = the_reply.dislikes.count()

        return reply_dislikes
