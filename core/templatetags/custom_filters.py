from django import template

from core.models import Book

register = template.Library()


@register.filter(name='in_user_favorites')
def in_user_favorites(book, user):
    try:
        fetchedBook = Book.objects.get(google_id=book['id'])
        return user.favorite_set.filter(book_id=fetchedBook.id).exists()
    except Book.DoesNotExist:
        return False



