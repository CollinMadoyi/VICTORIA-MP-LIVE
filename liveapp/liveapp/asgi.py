"""
ASGI config for liveapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Replace with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liveapp.settings')

application = ProtocolTypeRouter({
    # Handles standard HTTP requests (HTML/CSS)
    "http": get_asgi_application(),
    
    # Handles the WebSocket connections for Video/Chat
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})