import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage

# Consumer are for channels as views are for django

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
            print("Connected",event)
            await self.send({
                "type" : "websocket.accept" 
                
                })
            # await asyncio.sleep(10)
            await self.send({
                "type" : "websocket.send",
                "text": "Hello World"
                
                })
    async def websocket_receive(self, event):
        # When a message is received from websocket
        print("receive",event)
    async def websocket_disconnect(self, event):
        #When the socket disconnects
        print("Disconnected",event)


