"""사람 정보 관리 Admin."""
from django.contrib import admin
from people.models import Person


# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """사용자 정보."""
