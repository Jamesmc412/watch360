from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from django.db.models import Q
import asyncio

# This sets the model to be used
User = get_user_model()

#Class for Chat
class ChatConsumer(AsyncWebsocketConsumer):
    #Function for setting up connection
    async def connect(self):
        self.roomGroupName = f"user_{self.scope['user'].username}"
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
        await self.accept()
        
        await self.send(text_data=json.dumps({
            "type": "status",
            "message": "WebSocket connected and group joined."
        }))

        receiver_name = self.scope['url_route']['kwargs'].get('receiver')
        if receiver_name:
            await self.send_chat_history(receiver_name)

    #Function for setting up the receiver end
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Handle history load request
        if text_data_json.get("type") == "load_history":
            friend_name = text_data_json.get("friend_name")
            if friend_name:
                await self.send_chat_history(friend_name)
            return

        if 'message' in text_data_json and 'sender' in text_data_json and 'receiver' in text_data_json:
            message = text_data_json["message"]
            sender_username = text_data_json["sender"]
            receiver_username = text_data_json["receiver"]

            # Define room based on sender and receiver
            usernames = sorted([sender_username, receiver_username])
            conversation_room = f"chat_{usernames[0]}_{usernames[1]}"

            if self.roomGroupName != conversation_room:
                # Leave the current group if necessary
                if self.roomGroupName:
                    await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)
                
                self.roomGroupName = conversation_room
                await self.channel_layer.group_add(self.roomGroupName, self.channel_name)

            # Save and broadcast the message
            await self.save_message(sender_username, receiver_username, message)
            print(f"Message saved: {message} from {sender_username} to {receiver_username}")
            
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "new_message",
                    "message": message,
                    "sender": sender_username,
                    "receiver": receiver_username
                }
            )
            print("Message broadcasted to group:", self.roomGroupName)

            #pip install asyncio
            # Add a minimal delay for synchronization
            await asyncio.sleep(0)
            
            await self.send(text_data=json.dumps({
                "type": "new_message",
                "message": message,
                "sender": sender_username,
                "receiver": receiver_username
            }))
            print("Message sent back to sender:", message)

    #Sets up what is stored in database and the message handling
    async def new_message(self, event):
        # Extract message details from the event
        message = event.get("message")  # Use .get() to safely retrieve the key
        sender = event.get("sender")
        receiver = event.get("receiver")

        # Ensure these fields exist; if not, you can log an error or handle it appropriately
        if message is None or sender is None or receiver is None:
            print("Missing message, sender, or receiver in the event data:", event)
            return

        # Debugging log to verify the broadcast was received
        print(f"Broadcasted message received in new_message for {self.roomGroupName}")

        # Send the message to WebSocket clients in the room
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": message,
            "sender": sender,
            "receiver": receiver
        }))
        print("Message sent to WebSocket client:", message)


    #Displays the Chat History
    @sync_to_async
    def get_chat_history(self, friend_name):
        try:
            sender = self.scope["user"]
            receiver = User.objects.get(username=friend_name)
            messages = Message.objects.filter(
                (Q(sender=sender) & Q(receiver=receiver)) |
                (Q(sender=receiver) & Q(receiver=sender))
            ).order_by('timestamp')
            return list(messages.values('sender__username', 'receiver__username', 'content', 'timestamp'))
        except User.DoesNotExist as e:
            print(f"User not found in chat history: {e}")
            return []

    #Sets up sending to the user
    async def send_chat_history(self, friend_name):
        messages = await self.get_chat_history(friend_name)
        formatted_messages = [
            {
                "sender": msg["sender__username"],
                "receiver": msg["receiver__username"],
                "message": msg["content"],
            }
            for msg in messages
        ]
        await self.send(text_data=json.dumps({
            "type": "chat_history",
            "messages": formatted_messages
        }))

    #Saves the message for use
    @sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=sender, receiver=receiver, content=message)
        except User.DoesNotExist as e:
            print(f"Error saving message: {e}")

    #Disconnects the User if chat is closed
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)