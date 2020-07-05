"""인맥 관리 뷰."""
from django.db.models import TextChoices
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_settings
from people.models import Person
from people.serializer import PersonSerializer
from rest_framework.schemas.openapi import SchemaGenerator
from rest_framework.viewsets import ModelViewSet

from dashboard.inspectors import ExampleInspector


class MyAutoSchema(SwaggerAutoSchema):
    """예제를 추가해주는 Inspector 를 추가."""

    field_inspectors = [ExampleInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS


class Gender(TextChoices):
    """성별 Choice."""

    MALE = "Male", "남성"
    FEMALE = "Female", "여성"


# Create your views here.
class PersonViewSet(ModelViewSet):
    """사람 ViewSet."""

    generator = SchemaGenerator(title="Person API")
    # schema = generator.get_schema()

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    swagger_schema = MyAutoSchema
