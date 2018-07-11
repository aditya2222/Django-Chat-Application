import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


# Consumer are for channels as views are for django

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = "thread_{}".format(thread_obj.id)
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name  # default attribute of channels
        )

        await self.send({
            "type": "websocket.accept"

        })

        # await asyncio.sleep(10)

    async def websocket_receive(self, event):
        # When a message is received from websocket
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)  # Returns Dictionary Of Data that is loaded from the frontend
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
                await self.create_chat_message(user, msg)
            myResponse = {
                'message': msg,
                'username': username
            }

            # broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )

    async def chat_message(self, event):
        # sends the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        # When the socket disconnects
        print("Disconnected", event)

    @database_sync_to_async  # this is done to prevent memeory leaks,overload the database,open too many connections,etc
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)
