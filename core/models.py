from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    google_id = models.CharField(unique=True)
    title = models.TextField()
    thumbnail = models.URLField(max_length=9000, null=True)
    has_download_link = models.BooleanField(default=False)
    download_link = models.URLField(null=True)
    isbn = models.TextField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')
