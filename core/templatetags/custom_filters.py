from django import template
from urllib.parse import urlencode
from core.models import Book, Comment

register = template.Library()


@register.filter(name='encode_url')
def encode_url(url):
    return urlencode('http://localhost:8000/book/'+url)


@register.filter(name='in_user_favorites')
def in_user_favorites(book, user):
    try:
        fetchedBook = Book.objects.get(google_id=book['id'])
        return user.favorite_set.filter(book_id=fetchedBook.id).exists()
    except Book.DoesNotExist:
        return False


@register.filter(name='book_comments')
def book_comments(google_book):
    try:
        # Get the book with the specified title
        book = Book.objects.get(google_id=google_book['id'])
    except Book.DoesNotExist:
        # Book not found, return an empty queryset
        return Comment.objects.none()
    else:
        # Retrieve comments for the specified book
        return Comment.objects.filter(book=book).select_related('user').order_by('-createdAt')
