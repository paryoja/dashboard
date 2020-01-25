from django.contrib import admin

from . import models

admin.site.register(models.AuthUser)
admin.site.register(models.Boards)
admin.site.register(models.BoardCategories)
admin.site.register(models.Link)
admin.site.register(models.Lotto)
admin.site.register(models.Paper)
admin.site.register(models.Stock)
admin.site.register(models.Book)
admin.site.register(models.Image)
admin.site.register(models.PeopleImage)
admin.site.register(models.PokemonImage)
admin.site.register(models.Category)
admin.site.register(models.APIServers)
admin.site.register(models.Rating)
admin.site.register(models.DeepLearningModel)