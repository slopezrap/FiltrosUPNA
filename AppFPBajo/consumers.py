"""
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tasks import updateData
import json

class Consumidor(WebsocketConsumer):
    def connect(self):
        self.nombre_grupo = 'grupo'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            'grupo',
            self.channel_name
        )
        self.accept()
        print("Conexion aceptada")
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            'grupo',
            self.channel_name
        )
        print("Conexion desconectada")
        
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        #updateData.delay(message)
        
        #Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            'grupo',
             {
                 'type': 'post_socket',
                 'message': message
                 })
        
      
    # Receive message from room group
    def post_socket(self, event):
        print(event)
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import MensajeAlGrupo

class Consumidor(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            'grupo',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'grupo',
            self.channel_name
         )
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if str(message) == "hola":
            MensajeAlGrupo.delay()
        else:
            
            # Send message to room group
            await self.channel_layer.group_send(
                'grupo',
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
            
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))