from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.services import get_popular_books, get_book_details, scrape_download_content, scrape_urls
from .forms import SignupForm, CommentForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import Book, Favorite, Comment


def index(request):
    max_results_per_page = 9

    page = int(request.GET.get('page', 1))
    filterBy = request.GET.get('filterBy', None)
    searchTxt = request.GET.get('searchTxt', None)

    books, count, data = get_popular_books(page * max_results_per_page, max_results_per_page, filterBy, searchTxt)
    print(books, count, data)

    context = {
        'page': page,
        'books': enumerate(books),
        'has_previous': 9 * page > 0,
        'has_next': count - 9 * (page + 1) > 0,
        'next_page_number': page + 1,
        'previous_page_number': page - 1,
        'total_books': count,
        'first_page_showen_books': 9 * page-1,
        'last_page_showen_books': 9 * page,
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
def update_user(request):
    last_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(last_url)
    else:
        form = CustomUserChangeForm(instance=request.user)

    return redirect(last_url)


@login_required
def change_password(request):
    last_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(last_url)
    else:
        form = CustomPasswordChangeForm(request.user)

    return redirect(last_url)


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
def add_comment(request, book_google_id):
    bookDB = None
    if not Book.objects.filter(google_id=book_google_id).exists():
        googleBook = get_book_details(book_google_id)
        bookDB = Book.objects.create(
            google_id=googleBook['id'],
            thumbnail=googleBook['thumbnail'],
            title=googleBook['title'],
            isbn=googleBook['isbn'],
        )

    if bookDB is None:
        bookDB = Book.objects.get(google_id=book_google_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.book = bookDB
                comment.user = request.user
                comment.save()

    return redirect('book', google_book_id=book_google_id)


@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirect to the book details page or wherever you want to go
            return redirect('book', google_book_id=comment.book.google_id)


@login_required
def remove_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    book_id = comment.book.google_id
    comment.delete()

    return redirect('book', google_book_id=book_id)


def logout_view(request):
    logout(request)
    return redirect('index')


def generate_download_link(request, book_google_id):
    bookTarget = get_book_details(book_google_id)

    for isbn in bookTarget.get('isbn_list'):
        url_to_scrape = f'https://libgen.is/search.php?req={isbn}&open=3&res=25&view=simple&phrase=1&column=def'
        print("url_to_scrape:", url_to_scrape)
        result_urls = scrape_urls(url_to_scrape)
        print("result_urls:", result_urls)
        result_content = scrape_download_content(result_urls)
        print("download_link:", result_content)
        if result_content is not None:
            return render(request, 'core/download_book.html', {'book': bookTarget, 'download_link': result_content})

        return render(request, 'core/download_book.html', {'book': bookTarget, 'download_link': None})
