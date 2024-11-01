import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from watchapp.routing import websocket_urlpatterns  # Import WebSocket routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol
    "websocket": AuthMiddlewareStack(  # WebSocket protocol
        URLRouter(websocket_urlpatterns)
    ),
})
