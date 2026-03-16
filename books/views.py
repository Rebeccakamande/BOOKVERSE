from django.shortcuts import render, get_object_or_404
import random
from django.contrib.auth.decorators import login_required
from .models import Category, Book
from django.core.paginator import Paginator

from django.shortcuts import render
from books.models import Book, Category

def library_view(request):
    # Fetch all categories that have at least one book
    categories = Category.objects.prefetch_related('books').filter(books__isnull=False).distinct()

    library_data = []

    for category in categories:
        # Get the latest 8 books for each category
        books = category.books.all().order_by('-id')[:8]
        library_data.append({
            'category': category,
            'books': books
        })

    context = {
        'library_data': library_data
    }
    return render(request, 'books/library.html', context)

def category_books(request, slug):
    # Get the category
    category = get_object_or_404(Category, slug=slug)

    # All books in this category
    books = Book.objects.filter(categories=category).order_by('-id')

    # Paginate: 10 books per page
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')  # ?page=2
    page_obj = paginator.get_page(page_number)

    # Render template
    context = {
        "category": category,
        "page_obj": page_obj  # must match template variable
    }

    return render(request, 'books/category_books.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    context = {
        'book': book
    }

    return render(request, 'books/book_detail.html', context)