"""Chatbot 설정 및 학습용 데이터 모델."""
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(models.Model):
    """단어 모델."""

    added_date = models.DateTimeField("date added", auto_now_add=True)

    text = models.TextField("text")
    count = models.IntegerField("count", default=0)

    def __str__(self):
        return self.text


class Wiki(models.Model):
    """위키 데이터."""

    class WikiSource(models.TextChoices):
        """위키 데이터 타입."""

        NAMU = "NAMU", _("Namu")
        WIKIPEDIA = "WIKIPEDIA", _("Wikipedia")

    source = models.CharField(max_length=20, choices=WikiSource.choices)
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=300)


class People(models.Model):
    """사람에 대한 정보."""

    name = models.CharField(max_length=100)
    information = JSONField(null=True, blank=True)


class Match(models.Model):
    """경기 정보."""

    line_up = models.TextField()
    information = models.TextField()


class Player(models.Model):
    """선수 정보."""

    name = models.TextField()


class Lineup(models.Model):
    """라인업."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Match, on_delete=models.CASCADE)
    is_substitute = models.BooleanField()
    is_participated = models.BooleanField()
