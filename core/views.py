from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.services import get_popular_books, get_book_details
from .forms import SignupForm
from .models import Book, Favorite, Comment


def index(request):
    max_results_per_page = 9

    # Get the current page from the query parameters or default to 1

    page = int(request.GET.get('page', 0))
    filterBy = request.GET.get('filterBy', None)
    searchTxt = request.GET.get('searchTxt', None)

    books, count = get_popular_books(page * max_results_per_page, max_results_per_page, filterBy, searchTxt)

    context = {
        'page': page,
        'books': enumerate(books),
        'has_previous': 9 * page > 0,
        'has_next': count - 9 * (page + 1) > 0,
        'next_page_number': page + 1,
        'previous_page_number': page - 1,
        'total_books': count,
        'first_page_showen_books': 9 * page,
        'last_page_showen_books': 9 * (page + 1),
        'filterBy': filterBy,
        'searchTxt': searchTxt
    }

    return render(request, 'core/index.html', context)


@login_required
def book(request, google_book_id):
    googlBook = get_book_details(google_book_id)
    return render(request, '../templates/core/book.html', {'book': googlBook})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = SignupForm()
    return render(request, '../templates/core/signup.html', {'form': form})


@login_required
def add_to_favorites(request, book_id):
    if not Book.objects.filter(google_id=book_id).exists():
        googleBook = get_book_details(book_id)
        newBook = Book.objects.create(
            google_id=googleBook['id'],
            thumbnail=googleBook['thumbnail'],
            title=googleBook['title'],
            isbn=googleBook['isbn'],
        )
        Favorite.objects.create(user=request.user, book=newBook)

        return redirect('book', google_book_id=book_id)
    else:
        fetchedBook = Book.objects.get(google_id=book_id)

        # Check if the book is already in user's favorites
        if not Favorite.objects.filter(user=request.user, book=fetchedBook).exists():
            Favorite.objects.create(user=request.user, book=fetchedBook)

        return redirect('book', google_book_id=book_id)


def contact(request):
    return render(request, '../templates/core/contact.html')


@login_required
def remove_from_favorites(request, book_id):
    fetchedBook = Book.objects.get(google_id=book_id)
    favorite = Favorite.objects.get(user=request.user, book=fetchedBook)
    favorite.delete()

    return redirect('book', google_book_id=book_id)


@login_required
def favorites(request):
    favorite_books = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'core/favorites.html', {'favorite_books': favorite_books})


@login_required
def add_comment_to_book(request, book_id):
    content = request.POST.get('content')
    bookDB = None
    if not Book.objects.filter(google_id=book_id).exists():
        googleBook = get_book_details(book_id)
        bookDB = Book.objects.create(
            google_id=googleBook['id'],
            thumbnail=googleBook['thumbnail'],
            title=googleBook['title'],
            isbn=googleBook['isbn'],
        )

    Favorite.objects.create(user=request.user, book=bookDB, content=content)
    return redirect('book', google_book_id=book_id)
