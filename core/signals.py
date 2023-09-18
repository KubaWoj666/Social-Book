import json
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

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

        async_to_sync(channel_layers.group_send(
            'user', {
                "type": "send_online_status",
                "value": json.dumps(data, default=str)
            }
        ))
