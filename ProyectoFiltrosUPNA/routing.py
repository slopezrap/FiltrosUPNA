from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from AppFPBajo.consumers import Consumidor


application = ProtocolTypeRouter({
    "websocket":
        URLRouter([
            path("filtros/Crear_FPB/", Consumidor),
        ]),
})

