import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import get_template

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
        pass
        
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        request_id_user = data["request_user_id"]
        print("reciver", request_id_user)
    

    async def user_like_post(self, event):
        data = json.loads(event.get("value"))
        useername = data["user_who_like_post"]
        print(useername)
        await self.send(text_data=useername)