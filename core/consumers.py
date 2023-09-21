import uuid
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import get_template
from channels.db import database_sync_to_async

from .models import Likes, Post

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return
        self.group_name = "user-notifications"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):

        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        
    async def user_joined(self, event):
        # await self.send(text_data=event["text"])
        html = get_template("core/partials/notification.html").render(
            context={
                "username": event["text"]
            }
            )
        await self.send(text_data=html)


class LikeNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.request_user_id = self.scope["user"].id
        self.group_name = "like-notification"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        request_id_user = data["request_user_id"]
        # post= self.post_id
        print("reciver", request_id_user)
        # await self.save_like(request_id_user, post, True)

    

    async def user_like_post(self, event):
        data = json.loads(event.get("value"))
        username = data["user_who_like_post"]
        post_id = data["post_id"]
        post_id_uuid = uuid.UUID(post_id)
        post_title = data["post_title"]
        post_owner = data["post_owner"]

        # post_title = await self.get_post(post_id_uuid)
        

        print(post_id_uuid)
        print(username, )
        await self.send(text_data=json.dumps({
            "username": username,
            "post_id": post_id,
            "post_title": post_title,
            "post_owner": post_owner
            # "post_title":post_title
        }))
    
    # @database_sync_to_async
    # def save_like(user_id, post_id, liked):
    #     like = Likes.objects.create(user=user_id, post=post_id, liked=True)
    #     like.save()

    @database_sync_to_async
    def get_post(id):
        post = Post.objects.get(id=id)
        return post.title