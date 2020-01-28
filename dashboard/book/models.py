from django.contrib.postgres import fields
from django.db import models


class Link(models.Model):
    added_date = models.DateTimeField('date added', auto_now_add=True)
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
        db_table = 'book_auth_user'


class Boards(models.Model):
    category = models.ForeignKey('BoardCategories', models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    title = models.CharField(max_length=300)
    content = models.TextField()
    registered_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'boards'


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
        db_table = 'board_categories'


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
    url = models.URLField(unique=True, max_length=400)
    title = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    page = models.CharField(max_length=30)
    selected = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.url)


class PokemonImage(models.Model):
    url = models.URLField(unique=True, max_length=400)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    original_label = models.CharField(max_length=100)
    modified_label = models.CharField(max_length=100, null=True, blank=True)
    classified = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.url)


class Image(models.Model):
    url = models.URLField(unique=True, max_length=400)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

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
