from django.contrib.postgres import fields
from django.db import models
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    added_date = models.DateTimeField("date added", auto_now_add=True)
    url = models.URLField()

    content_type = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    visit_count = models.IntegerField(default=0)

    def __str__(self):
        return self.description


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254)
    date_joined = models.DateTimeField()
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=45)
    date_of_birth = models.DateTimeField()

    class Meta:
        db_table = "book_auth_user"


class Boards(models.Model):
    category = models.ForeignKey("BoardCategories", models.DO_NOTHING)
    user = models.ForeignKey("AuthUser", models.DO_NOTHING)
    title = models.CharField(max_length=300)
    content = models.TextField()
    registered_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "boards"


class BoardCategories(models.Model):
    category_type = models.CharField(max_length=45)
    category_code = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    category_desc = models.CharField(max_length=200)
    list_count = models.IntegerField(blank=True, null=True)
    authority = models.IntegerField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "board_categories"


class Lotto(models.Model):
    draw_number = models.IntegerField()
    numbers = fields.JSONField()


class Stock(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)


class Paper(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    slide = models.URLField(blank=True, null=True)
    authors = fields.ArrayField(models.CharField(max_length=20), blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Book(models.Model):
    name = models.TextField()
    author = models.CharField(max_length=20)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}: 저자 {}".format(self.name, self.author)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name)


class PeopleImage(models.Model):
    def get_user_id(self):
        return self.url.split("/")[5]

    url = models.URLField(unique=True, max_length=400)
    title = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    page = models.CharField(max_length=30)
    selected = models.BooleanField(null=True, blank=True)
    user_id = models.CharField(max_length=20)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.user_id = self.get_user_id()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "{}".format(self.url)


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    checked = models.BooleanField(default=False)


class PokemonImage(models.Model):
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
    url = models.URLField(unique=True, max_length=400)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return "{} ({})".format(self.title, self.url)


class APIServers(models.Model):
    ip = models.CharField(max_length=200, unique=False)
    title = models.CharField(max_length=20, unique=True)
    endpoint = models.CharField(max_length=100)
    port = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.title, self.ip)


class DeepLearningModel(models.Model):
    domain = models.TextField(max_length=20)
    version = models.TextField(max_length=10)
    latest = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} (latest {})".format(self.domain, self.version, self.latest)


class Rating(models.Model):
    deep_model = models.ForeignKey(DeepLearningModel, on_delete=models.CASCADE)
    image = models.ForeignKey(PeopleImage, on_delete=models.CASCADE)
    data = fields.JSONField()
    positive = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {} {}".format(self.id, self.positive, self.image.title)


class PokemonRating(models.Model):
    deep_model = models.ForeignKey(DeepLearningModel, on_delete=models.CASCADE)
    image = models.ForeignKey(PokemonImage, on_delete=models.CASCADE)
    data = fields.JSONField()
    positive = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {} {}".format(self.id, self.positive, self.image.title)

    def get_prob(self):
        if "classification" in self.data and "class_names" in self.data:
            result_list = []
            if isinstance(self.data["classification"], list):
                for class_name, idx in self.data["class_names"].items():
                    result_list.append((class_name, self.data["classification"][idx]))
                result_list = sorted(result_list, key=lambda x: x[1], reverse=True)

            return result_list


class Currency(models.Model):
    class CurrencyChoices(models.TextChoices):
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
        return self.from_amount / self.to_amount


class Wine(models.Model):
    class RatingChoices(models.IntegerChoices):
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
    date = models.DateField()
    confirmed = models.IntegerField()
    death = models.IntegerField()
    country = models.CharField(default="Korea", max_length=20)


class BestPhoto(models.Model):
    img = models.ForeignKey(PeopleImage, on_delete=models.CASCADE)
    url = models.URLField(unique=True, max_length=400)


class TodoItem(models.Model):
    class StatusChoices(models.TextChoices):
        DONE = "Done", _("Done")
        TODO = "Todo", _("Todo")
        IN_PROGRESS = "In Progress", _("In Progress")

    title = models.CharField(max_length=100)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
