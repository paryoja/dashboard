"""Chatbot 모델 Admin."""
# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    """단어를 Admin Page 에서 제공."""

    list_display = ("added_date", "text", "count")
