# myproject/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from myapp.consumer import MyConsumer

application = ProtocolTypeRouter({
    # WebSocket使用的协议类型是“websocket”，将它放在第一位
    "websocket": URLRouter([
        path("ws/", MyConsumer.as_asgi()),
    ]),
})