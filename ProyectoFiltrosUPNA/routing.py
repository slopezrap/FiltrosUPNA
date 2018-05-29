from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from AppFPBajo.consumers import Consumidor
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
    
        URLRouter([
            path("filtros/Crear_FPB/", Consumidor),
        ]),
    ),  
})

