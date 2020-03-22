from django.contrib import admin

from . import models

admin.site.register(models.AuthUser)
admin.site.register(models.Category)
admin.site.register(models.Wine)


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "file", "slide", "authors")


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "checked")


@admin.register(models.Lotto)
class LottoAdmin(admin.ModelAdmin):
    list_display = ("draw_number", "numbers")


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("added_date", "url", "description", "content_type")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "year")


@admin.register(models.APIServers)
class APIServerAdmin(admin.ModelAdmin):
    list_display = ("title", "ip", "port", "endpoint")


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Date information", {"fields": ["date"]}),
        ("From", {"fields": ["from_currency", "from_amount"]}),
        ("To", {"fields": ["to_currency", "to_amount"]}),
        ("Rate", {"fields": ["currency_rate"]}),
    ]
    list_display = ("date", "from_amount", "to_amount", "currency_rate")


@admin.register(models.DeepLearningModel)
class DeepLearningModelAdmin(admin.ModelAdmin):
    list_display = ("domain", "version", "latest")


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("url", "title")


@admin.register(models.PeopleImage)
class PeopleImageAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "selected")


@admin.register(models.PokemonImage)
class PokemonImageAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "original_label", "classified")


@admin.register(models.Corona)
class CoronaAdmin(admin.ModelAdmin):
    list_display = ("date", "confirmed", "death", "country")


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    raw_id_fields = ("image",)


@admin.register(models.PokemonRating)
class PokemonRatingAdmin(admin.ModelAdmin):
    raw_id_fields = ("image",)
