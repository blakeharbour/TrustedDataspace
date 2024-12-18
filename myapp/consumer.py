# myapp/consumers.py

import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        WebSocket连接建立时执行。
        """
        await self.accept()

    async def disconnect(self, code):
        """
        WebSocket连接中断时执行。
        """
        pass

    async def receive(self, text_data=None, bytes_data=None):
        """
        当从WebSocket连接接收到数据时执行。
        """
        # 解析WebSocket发送的JSON数据
        data = json.loads(text_data)
        # 从JSON数据中获取请求
        request = data['request']

        # 这里是处理请求的代码
        # ...

        # 发送响应到WebSocket连接
        response = {'status': 'OK', 'data': request}
        await self.send(json.dumps(response))