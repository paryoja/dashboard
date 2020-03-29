# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("added_date", "text", "count")
