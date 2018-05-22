from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




@shared_task
def MensajeAlGrupo():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'grupo',
            {
             "type": "chat.message", 
             "message": "Hello World"
             },
        )