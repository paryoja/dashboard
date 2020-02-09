from django.contrib import admin

from . import models

admin.site.register(models.AuthUser)
admin.site.register(models.Lotto)
admin.site.register(models.Paper)
admin.site.register(models.Category)
admin.site.register(models.Rating)
admin.site.register(models.Wine)
admin.site.register(models.Corona)


class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


admin.site.register(models.Stock, StockAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('added_date', 'url', 'description', 'content_type')


admin.site.register(models.Link, LinkAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'year')


admin.site.register(models.Book, BookAdmin)


class APIServerAdmin(admin.ModelAdmin):
    list_display = ('title', 'ip', 'port', 'endpoint')


admin.site.register(models.APIServers, APIServerAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = [('Date information', {'fields': ['date']}),
                 ('From', {'fields': ['from_currency', 'from_amount']}),
                 ('To', {'fields': ['to_currency', 'to_amount']}),
                 ('Rate', {'fields': ['currency_rate']})]
    list_display = ('date', 'from_amount', 'to_amount', 'currency_rate')


admin.site.register(models.Currency, CurrencyAdmin)


class DeepLearningModelAdmin(admin.ModelAdmin):
    list_display = ('domain', 'version', 'latest')


admin.site.register(models.DeepLearningModel, DeepLearningModelAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')


admin.site.register(models.Image, ImageAdmin)


class PeopleImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'selected')


admin.site.register(models.PeopleImage, PeopleImageAdmin)


class PokemonImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'original_label', 'classified')


admin.site.register(models.PokemonImage)
