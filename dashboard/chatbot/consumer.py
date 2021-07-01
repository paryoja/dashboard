"""웹소켓 consumer."""
import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """채팅 socket consumer."""

    def connect(self):
        """웹 소켓 연결 시 실행."""
        self.accept()

    def disconnect(self, close_code):
        """웹 소켓 연결 종료 시 실행."""
        pass

    def receive(self, text_data=None, bytes_data=None):
        """클라이언트로부터 메세지를 받을 시 실행."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # 클라이언트로부터 받은 메세지를 다시 클라이언트로 보내준다.
        self.send(text_data=json.dumps({"message": message}))
