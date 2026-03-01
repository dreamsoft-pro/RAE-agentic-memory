import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.machine_code = self.scope['url_route']['kwargs'].get('machine_code')
        
        if self.machine_code:
            self.group_name = f"machine_{self.machine_code}"
        else:
            self.group_name = "all_machines"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def machine_telemetry(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))
