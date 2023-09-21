import json
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Post, Likes

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync


@receiver(post_save, sender=Profile)
def send_online_status(sender, instance, created ,**kwargs):
    if not created:
        channel_layers = get_channel_layer()
        user = instance.user.username
        user_status = instance.online_status
        
        data = {
            "username": user,
            "status": user_status
        }

        async_to_sync(channel_layers.group_send)(
            'user', {
                "type": "send_online_status",
                "value": json.dumps(data, default=str)
            }
        )


@receiver(post_save, sender=Profile)
def send_notification_on_signup(sender, created, instance, **kwargs):
    if created:
        chanel_layer = get_channel_layer()
        group_name = "user-notifications"

        event = {
            'type': "user_joined",
            "text": instance.user.username
        }

        async_to_sync(chanel_layer.group_send)(group_name, event)



@receiver(post_save, sender=Likes)
def send_like_notification(sender, created, instance, **kwargs):
    if created:
        chanel_layer = get_channel_layer()
        group_name = "like-notification"

        username = instance.user.username
        post_id = str(instance.post.id)
        post = Post.objects.get(id=post_id)
        post.liked = True
        post_owner = post.user.username
        post_title = post.title
        post.save()
        print(username, post_id)

        data = {
            "user_who_like_post": username,
            "post_id": post_id,
            "post_title": post_title,
            "post_owner": post_owner,
            "liked": "true"
        }


        async_to_sync(chanel_layer.group_send)(
            group_name, {
                "type": "user_like_post",
                "value": json.dumps(data)
            }
        )
