"""
ASGI config for Discord_QuizBot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from Discord_admin import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Discord_QuizBot.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AllowedHostsOriginValidator(  # Handle WebSocket connections
        AuthMiddlewareStack(  # Apply authentication middleware
            URLRouter(
                routing.websocket_urlpatterns  # Point to your WebSocket routing
            )
        )
    ),
})