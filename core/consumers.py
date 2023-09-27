import uuid
import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
        

    async def user_like_post(self, event):
        data = json.loads(event.get("value"))
        username = data["user_who_like_post"]
        post_id = data["post_id"]
        post_title = data["post_title"]
        post_owner = data["post_owner"]

        await self.send(text_data=json.dumps({
            "username": username,
            "post_id": post_id,
            "post_title": post_title,
            "post_owner": post_owner
        }))

    
    async def user_follow(self, event):
        data = json.loads(event.get("value"))
        request_user = data["request_user"]
        following_user = data["following_user"]

        await self.send(text_data=json.dumps({
            "request_user": request_user,
            "following_user": following_user,
        }))
        

    async def user_comment(self, event):
        data = json.loads(event.get("value"))

        comment_owner = data["comment_owner"]
        commented_post_title = data["commented_post_title"]
        commented_post_owner = data["commented_post_owner"]
        
        await self.send(text_data=json.dumps({
            "comment_owner": comment_owner,
            "commented_post_title":commented_post_title,
            "commented_post_owner": commented_post_owner
        }))
    
   