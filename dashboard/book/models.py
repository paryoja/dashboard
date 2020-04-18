"""Book 모델."""

from django.contrib.postgres import fields
from django.db import models
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    """유용한 Link."""

    added_date = models.DateTimeField("date added", auto_now_add=True)
    url = models.URLField()

    content_type = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    visit_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        """설명만 제공."""
        return str(self.description)


class Lotto(models.Model):
    """로또 정보."""

    draw_number = models.IntegerField()
    numbers = fields.JSONField()


class Stock(models.Model):
    """주식 정보."""

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)


class Paper(models.Model):
    """논문 정보."""

    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    slide = models.URLField(blank=True, null=True)
    authors = fields.ArrayField(models.CharField(max_length=20), blank=True, null=True)

    def __str__(self):
        """Title 만 제공."""
        return str(self.title)


class Book(models.Model):
    """읽을 만한 책."""

    name = models.TextField()
    author = models.CharField(max_length=20)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        """제목과 저자 정보."""
        return "{}: 저자 {}".format(self.name, self.author)


class Category(models.Model):
    """이미지 카테고리."""

    name = models.CharField(max_length=200)

    def __str__(self):
        """이미지 카테고리명."""
        return str(self.name)


class PeopleImage(models.Model):
    """이미지."""

    url = models.URLField(unique=True, max_length=400)
    title = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    page = models.CharField(max_length=30)
    selected = models.BooleanField(null=True, blank=True)
    user_id = models.CharField(max_length=20)
    content_parsed = models.BooleanField(null=True, blank=True, default=None)

    def get_user_id(self):
        """URL 의 5번째 항목."""
        return self.url.split("/")[5]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """저장시 user_id 세팅."""
        self.user_id = self.get_user_id()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.url)


class User(models.Model):
    """User 정보."""

    username = models.CharField(max_length=30, unique=True)
    checked = models.BooleanField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return "{} {}".format(self.username, self.checked)


class PokemonImage(models.Model):
    """포켓몬 이미지."""

    url = models.URLField(unique=True, max_length=400)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    original_label = models.CharField(max_length=100)
    modified_label = models.CharField(max_length=100, null=True, blank=True)
    classified = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.url)


class Image(models.Model):
    """Image Base."""

    url = models.URLField(unique=True, max_length=400)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return "{} ({})".format(self.title, self.url)


class APIServers(models.Model):
    """API 서버 위치."""

    ip = models.CharField(max_length=200, unique=False)
    title = models.CharField(max_length=20, unique=True)
    endpoint = models.CharField(max_length=100)
    port = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.title, self.ip)


class DeepLearningModel(models.Model):
    """딥러닝 모델."""

    domain = models.TextField(max_length=20)
    version = models.TextField(max_length=10)
    latest = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} (latest {})".format(self.domain, self.version, self.latest)


class Rating(models.Model):
    """이미지 선택 정보."""

    deep_model = models.ForeignKey(DeepLearningModel, on_delete=models.CASCADE)
    image = models.ForeignKey(PeopleImage, on_delete=models.CASCADE)
    data = fields.JSONField()
    positive = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {} {}".format(self.id, self.positive, self.image.title)


class PokemonRating(models.Model):
    """포켓몬 이미지 분류 정보."""

    deep_model = models.ForeignKey(DeepLearningModel, on_delete=models.CASCADE)
    image = models.ForeignKey(PokemonImage, on_delete=models.CASCADE)
    data = fields.JSONField()
    positive = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {} {}".format(self.id, self.positive, self.image.title)

    def get_prob(self):
        """Class 별 확률 값 가져옴."""
        if "classification" in self.data and "class_names" in self.data:
            result_list = []
            if isinstance(self.data["classification"], list):
                for class_name, idx in self.data["class_names"].items():
                    result_list.append((class_name, self.data["classification"][idx]))
                result_list = sorted(result_list, key=lambda x: x[1], reverse=True)

            return result_list


class Currency(models.Model):
    """환전 내역."""

    class Meta:
        """Meta data for currency."""

        verbose_name_plural = "Currencies"

    class CurrencyChoices(models.TextChoices):
        """환전."""

        USD = "USD", _("USD")
        KRW = "KRW", _("KRW")

    date = models.DateField()
    from_currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.KRW
    )
    to_currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.USD
    )

    currency_rate = models.FloatField()
    from_amount = models.FloatField()
    to_amount = models.FloatField()

    def get_currency_rate(self):
        """환율 계산."""
        return self.from_amount / self.to_amount


class Wine(models.Model):
    """와인 정보."""

    class RatingChoices(models.IntegerChoices):
        """와인 평가 등급."""

        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.TextField()
    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    price = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)


class Corona(models.Model):
    """코로나 정보."""

    date = models.DateField()
    confirmed = models.IntegerField()
    death = models.IntegerField()
    country = models.CharField(default="Korea", max_length=20)


class BestPhoto(models.Model):
    """Best Photo 선택 정보."""

    img = models.ForeignKey(PeopleImage, on_delete=models.CASCADE)
    url = models.URLField(unique=True, max_length=400)


class TodoItem(models.Model):
    """할일 정보."""

    class StatusChoices(models.TextChoices):
        """할일의 status."""

        DONE = "Done", _("Done")
        TODO = "Todo", _("Todo")
        IN_PROGRESS = "In Progress", _("In Progress")

    title = models.CharField(max_length=100)
    status = models.CharField(
        choices=StatusChoices.choices, max_length=20, default=StatusChoices.TODO
    )
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
