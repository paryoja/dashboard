"""채팅을 위한 ASGI 세팅."""
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
    }
)
