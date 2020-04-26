"""Book Admin."""
from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe

from . import models

admin.site.register(models.Category)
admin.site.register(models.Wine)


@admin.register(models.TodoItem)
class TodoAdmin(admin.ModelAdmin):
    """할일 정리."""

    list_display = ("title", "status")


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    """논문정보."""

    list_display = ("title", "link", "file", "slide", "authors")


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """인스타 사용자 정보."""

    list_display = ("username", "checked")


@admin.register(models.Lotto)
class LottoAdmin(admin.ModelAdmin):
    """로또 정보."""

    list_display = ("draw_number", "numbers")


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    """주식 정보."""

    list_display = ("code", "name", "is_etf")


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    """링크 정보."""

    list_display = ("added_date", "url", "description", "content_type")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    """책 정보."""

    list_display = ("name", "author", "year")


@admin.register(models.APIServers)
class APIServerAdmin(admin.ModelAdmin):
    """API 서버 정보."""

    list_display = ("title", "ip", "port", "endpoint")


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """환전 정보."""

    fieldsets = [
        ("Date information", {"fields": ["date"]}),
        ("From", {"fields": ["from_currency", "from_amount"]}),
        ("To", {"fields": ["to_currency", "to_amount"]}),
        ("Rate", {"fields": ["currency_rate"]}),
    ]
    list_display = ("date", "from_amount", "to_amount", "currency_rate", "rate")

    def from_amount(self, obj):
        """Format from_amount."""
        return intcomma(floatformat(obj.from_amount))

    def rate(self, obj):
        """환율을 변환된 값으로 부터 계산한 값."""
        return "%.2f" % (float(obj.from_amount) / float(obj.to_amount))


@admin.register(models.DeepLearningModel)
class DeepLearningModelAdmin(admin.ModelAdmin):
    """딥러닝 모델 정보."""

    list_display = ("domain", "version", "latest")


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    """이미지 정보."""

    list_display = ("url", "title")


@admin.register(models.PeopleImage)
class PeopleImageAdmin(admin.ModelAdmin):
    """인스타 이미지 정보."""

    readonly_fields = ["insta_image"]

    list_display = ("id", "user_id", "title", "selected", "insta_image", "url")
    list_editable = ("selected",)
    list_filter = ("selected", "user_id")

    def insta_image(self, obj):
        """Add image add for admin page."""
        return mark_safe(f'<img src="{obj.url}"/>')


@admin.register(models.PokemonImage)
class PokemonImageAdmin(admin.ModelAdmin):
    """포켓몬 이미지."""

    list_display = ("url", "title", "original_label", "classified")


@admin.register(models.Corona)
class CoronaAdmin(admin.ModelAdmin):
    """코로나 정보."""

    list_display = ("date", "confirmed", "death", "country")


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    """이미지 분류 정보."""

    raw_id_fields = ("image",)


@admin.register(models.PokemonRating)
class PokemonRatingAdmin(admin.ModelAdmin):
    """포켓몬 분류 정보."""

    raw_id_fields = ("image",)


@admin.register(models.Lecture)
class LectureAdmin(admin.ModelAdmin):
    """강의 정보."""

    list_display = ("title", "status", "class_name", "number")


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    """은행 정보."""

    list_display = ("name",)


@admin.register(models.Saving)
class SavingAdmin(admin.ModelAdmin):
    """적금 정보."""

    list_display = (
        "date",
        "bank",
        "account_number",
        "principal",
        "interest",
        "interest_rate",
        "tax",
        "payment",
        "interest_minus_tax",
        "interest_rate_per_year",
    )

    def interest_rate(self, obj):
        """이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate * 100)

    def interest_rate_minus_tax(self, obj):
        """실이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate_minus_tax * 100)

    def interest_rate_per_year(self, obj):
        """연환산 이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate_per_year * 100)
