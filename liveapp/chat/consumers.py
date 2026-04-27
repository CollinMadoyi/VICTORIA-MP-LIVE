import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    # A simple global queue in Redis would be better, 
    # but for this demo, we use a class-level set.
    queue = []

    async def connect(self):
        self.room_name = None
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'find_match':
            await self.handle_matching()
        
        elif action in ['signal', 'chat_message']:
            # Forward WebRTC signals or chat messages to the partner
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "forward_message",
                    "data": data,
                    "sender_channel_name": self.channel_name
                }
            )

    async def handle_matching(self):
        if ChatConsumer.queue:
            partner_channel = ChatConsumer.queue.pop(0)
            self.room_group_name = f"room_{hash(self.channel_name)}"
            
            # Join both to the same group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_add(self.room_group_name, partner_channel)

            # Notify both users
            await self.channel_layer.group_send(
                self.room_group_name, 
                {"type": "match_found", "initiator": partner_channel}
            )
        else:
            ChatConsumer.queue.append(self.channel_name)
            await self.send(json.dumps({"status": "waiting"}))

    async def match_found(self, event):
        # The initiator starts the WebRTC Offer
        is_initiator = self.channel_name == event['initiator']
        await self.send(json.dumps({
            "action": "match_found",
            "is_initiator": is_initiator
        }))

    async def forward_message(self, event):
        # Don't send back to the person who sent it
        if self.channel_name != event['sender_channel_name']:
            await self.send(json.dumps(event['data']))

    async def disconnect(self, close_code):
        if self.channel_name in ChatConsumer.queue:
            ChatConsumer.queue.remove(self.channel_name)
        # Handle group cleanup logic here

# chat/consumers.py

async def disconnect(self, close_code):
    # Safely get channel_name; if it doesn't exist, set to None
    channel_name = getattr(self, 'channel_name', None)

    if channel_name:
        # Check if this specific channel is in your matching queue
        if channel_name in ChatConsumer.queue:
            ChatConsumer.queue.remove(channel_name)
        
        # Leave the Wi-Fi group if you joined one
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                channel_name
            )

    print(f"WebSocket disconnected with code: {close_code}")