"""채팅을 위한 ASGI 세팅."""
from chatbot import consumer
from django.conf.urls import url

websocket_urlpatterns = [
    url(r"^ws/chat/(?P<room_name>[^/]+)/$", consumer.ChatConsumer),
]
