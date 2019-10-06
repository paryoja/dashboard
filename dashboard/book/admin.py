from django.contrib import admin

from .models import AuthUser, Boards, BoardCategories

admin.site.register(AuthUser)
admin.site.register(Boards)
admin.site.register(BoardCategories)
