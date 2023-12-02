from django.shortcuts import render
from core.services import get_popular_books, get_book_details


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


def book(request, id):
    book = get_book_details(id)
    return render(request, '../templates/core/book.html', {'book': book})


def contact(request):
    return render(request, '../templates/core/contact.html')
