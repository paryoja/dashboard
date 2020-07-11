"""인맥 관리 뷰."""
from django.db.models import TextChoices
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema, swagger_settings
from people.models import Person
from people.serializer import PersonSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator
from rest_framework.viewsets import GenericViewSet

from dashboard.inspectors import ExampleInspector


class CustomSchema(AutoSchema):
    """스키마 변경 예."""

    def get_operation(self, path, method):
        """스키마 변경 시도."""
        operation = {}

        operation["operationId"] = self._get_operation_id(path, method)
        operation["description"] = self.get_description(path, method)

        operation["parameters"] = {"hi": "there"}
        operation["requestBody"] = {"content": "none"}
        operation["responses"] = {"200": {"content": {}}}
        return operation


class MyAutoSchema(SwaggerAutoSchema):
    """예제를 추가해주는 Inspector 를 추가."""

    field_inspectors = [ExampleInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS


class Gender(TextChoices):
    """성별 Choice."""

    MALE = "Male", "남성"
    FEMALE = "Female", "여성"


# Create your views here.
class PersonViewSet(GenericViewSet):
    """사람 ViewSet."""

    http_method_names = ["get", "post"]
    generator = SchemaGenerator(title="Person API")
    schema = CustomSchema

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    swagger_schema = MyAutoSchema

    def list(self, request, *args, **kwargs):
        """Get Request 에 대응."""
        return Response("Hello")

    @swagger_auto_schema(responses={404: "slug not found"})
    def create(self, request, *args, **kwargs):
        """Post Request 에 대응."""
        return Response("hi")

    @action(detail=False, methods=["post"], schema=None)
    def hi_there(self):
        """커스텀 연산."""
        pass
