from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Order.routing, Main.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            Order.routing.websocket_urlpatterns + Main.routing.websocket_urlpatterns
        ),
    ),
})