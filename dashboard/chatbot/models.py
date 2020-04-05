"""Chatbot 설정 및 학습용 데이터 모델."""
from django.db import models


class Word(models.Model):
    """단어 모델."""

    added_date = models.DateTimeField("date added", auto_now_add=True)

    text = models.TextField("text")
    count = models.IntegerField("count", default=0)

    def __str__(self):
        return self.text
