from django.contrib import admin
from .models import Book, Favorite,Comment

admin.site.register(Book)
admin.site.register(Favorite)
admin.site.register(Comment)
