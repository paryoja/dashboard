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


class Paper(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    slide = models.URLField(blank=True, null=True)
    authors = fields.ArrayField(models.CharField(max_length=20), blank=True, null=True)

    def __str__(self):
        return str(self.title)
