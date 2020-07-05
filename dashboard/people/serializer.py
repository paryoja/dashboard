"""인맥 관리 프로젝트의 모델 Serializer."""
from people.models import Person
from rest_framework.serializers import ModelSerializer


class PersonSerializer(ModelSerializer):
    """사람 객체를 처리하는 Serializer."""

    class Meta:
        """예제 추가."""

        model = Person
        exclude = ["created_at"]
        examples = {
            "id": 1,
            "name": "박윤재",
        }
