from django.db import models


class Word(models.Model):
    added_date = models.DateTimeField("date added", auto_now_add=True)

    text = models.TextField("text")
    count = models.IntegerField("count", default=0)

    def __str__(self):
        return self.text
