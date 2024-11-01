from django.urls import path, include
from watchapp.consumers import ChatConsumer  # Correct import

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
]