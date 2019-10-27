from django.contrib import admin

from .models import AuthUser, Boards, BoardCategories, Link, Lotto

admin.site.register(AuthUser)
admin.site.register(Boards)
admin.site.register(BoardCategories)
admin.site.register(Link)
admin.site.register(Lotto)