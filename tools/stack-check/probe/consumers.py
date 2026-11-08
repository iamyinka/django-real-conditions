from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EchoConsumer(AsyncJsonWebsocketConsumer):
    """Joins a group; anything sent to the group is pushed to every socket in it."""

    async def connect(self):
        await self.channel_layer.group_add("echo", self.channel_name)
        await self.accept()

    async def receive_json(self, content):
        await self.channel_layer.group_send("echo", {"type": "broadcast", "payload": content})

    async def broadcast(self, event):
        await self.send_json(event["payload"])
