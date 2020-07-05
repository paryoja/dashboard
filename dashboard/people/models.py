"""인맥 정리용 모델."""
from django.db import models


class Person(models.Model):
    """사람 객체."""

    name = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
