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


class LinkAdmin(admin.ModelAdmin):
    list_display = ('added_date', 'url', 'description', 'content_type')


class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = [('Date information', {'fields': ['date']}),
                 ('From', {'fields': ['from_currency', 'from_amount']}),
                 ('To', {'fields': ['to_currency', 'to_amount']}),
                 ('Rate', {'fields': ['currency_rate']})]
    list_display = ('date', 'from_amount', 'to_amount', 'currency_rate')


admin.site.register(models.Currency, CurrencyAdmin)
