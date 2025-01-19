import os
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter , ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import Chat.chat_modules.routing as aa
from .middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiveChatFaceAuth.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':JWTAuthMiddleware(
        URLRouter(
            aa.websocket_urlpatterns
        )
    )
})
