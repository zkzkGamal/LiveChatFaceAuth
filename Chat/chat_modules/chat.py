import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Chat.chat_modules.chech_auth import ChechAuth

checker = ChechAuth()
class ChatConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        self.room_name = self.scope['session']
        self.room_group_name = f"chat_{self.room_name}"
        if not checker(user = self.scope['user'], session = self.scope['session'] , key =self.scope["key"]):
            self.close(code=405 ,reason= "invalid argumants")
            return "invalid argumants"
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept("test")
    
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
