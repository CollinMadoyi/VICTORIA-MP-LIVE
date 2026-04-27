from django.urls import re_path
from . import consumers # We will create this next

websocket_urlpatterns = [
    # This matches the /ws/chat/ path in your JavaScript
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]