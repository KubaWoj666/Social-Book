import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatModel
from core.models import Profile

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = "chat_" + self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # await self.send(text_data=self.room_group_name)
        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        sender_username = data["sender_username"]

        await self.save_messages(sender_username, message, self.room_group_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
    
    @database_sync_to_async
    def save_messages(self, username, message, thread_name):
        
        ChatModel.objects.create(sender=username, message=message, thread_name=thread_name)
   


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data["username"]
        connection_type = data["type"]
        await self.change_online_status(username, connection_type)
    

    async def send_online_status(self, event):
        data = json.loads(event.get('value'))
        username = data["username"]
        online_status = data["status"]
        await self.send(text_data=json.dumps({
            "username": username,
            "online_status": online_status

        }))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)
   

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user_profile= Profile.objects.get(user__username=username)

        if c_type == "open":
            user_profile.online_status = True
            user_profile.save()
        else:
            user_profile.online_status = False
            user_profile.save()
