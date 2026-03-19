from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.shortcuts import render
from books.models import Book
from .models import ReadingProgress
import json
from django.http import JsonResponse
from django.contrib import messages


@login_required
def update_reading_status(request, book_id, status):
    """
    Updates a user's reading status for a book:
    - to_be_read
    - reading
    - completed

    Automatically creates a ReadingProgress object if it doesn't exist.
    Ensures status, current_page, and percentage stay consistent.
    Redirects to the dashboard after update.
    """

    # 1. Fetch the book
    book = get_object_or_404(Book, id=book_id)

    # 2. Get or create reading progress
    progress, created = ReadingProgress.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'status': status, 'current_page': 1, 'percentage': 0}
    )

    # 3. Update status
    progress.status = status

    # 4. Maintain consistency
    if status == 'to_be_read':
        progress.percentage = 0
        progress.current_page = 1

    elif status == 'reading':
        if progress.percentage == 100:  # reset if previously completed
            progress.percentage = 1
        if progress.current_page < 1:
            progress.current_page = 1
        # Track start time (optional)
        if not getattr(progress, 'started_at', None):
            try:
                progress.started_at = now()
            except:
                pass

    elif status == 'completed':
        progress.percentage = 100
        # Track completion time
        try:
            progress.completed_at = now()
        except:
            pass

    # 5. Save changes
    progress.save()

    # 6. Redirect to dashboard
    return redirect('dashboard')

@login_required
def dashboard_view(request):
    # Get all reading progress for this user
    progress_qs = ReadingProgress.objects.filter(user=request.user).select_related('book')

    # Filter by status
    to_be_read = progress_qs.filter(status='to_be_read')
    currently_reading = progress_qs.filter(status='reading')
    completed = progress_qs.filter(status='completed')

    context = {
        'to_be_read': to_be_read,
        'currently_reading': currently_reading,
        'completed': completed,
        'to_be_read_count': to_be_read.count(),
        'currently_reading_count': currently_reading.count(),
        'completed_count': completed.count(),
    }

    return render(request, 'reading/dashboard.html', context)

@login_required
def read_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # 🔥 CHECK IF FILE EXISTS
    if not book.file:
        messages.warning(request, "This book does not have a readable file yet.")
        return redirect('dashboard')


    progress, created = ReadingProgress.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={
            'status': 'reading',
            'current_page': 1,
            'percentage': 0
        }
    )

    #If user clicks "Start Reading"
    if progress.status == 'to_be_read':
        progress.status = 'reading'
        progress.save()

    return render(request, 'reading/reader.html', {
        'book': book,
        'progress': progress
    })

@login_required
def save_progress(request, book_id):
    if request.method == "POST":
        data = json.loads(request.body)

        page = data.get('page')
        percentage = data.get('percentage')

        progress = ReadingProgress.objects.get(
            user=request.user,
            book_id=book_id
        )

        progress.current_page = page
        progress.percentage = percentage

        
        if percentage >= 100:
            progress.status = 'completed'
        elif percentage > 0:
            progress.status = 'reading'

        progress.save()

        return JsonResponse({'status': 'success'})


@login_required
def dashboard_progress_api(request):
    progress_qs = ReadingProgress.objects.filter(user=request.user, status='reading').select_related('book')
    currently_reading = [
        {
            'book_id': p.book.id,
            'current_page': p.current_page,
            'percentage': p.percentage
        } for p in progress_qs
    ]
    return JsonResponse({
        'currently_reading': currently_reading,
        'currently_reading_count': progress_qs.count(),
        'completed_count': ReadingProgress.objects.filter(user=request.user, status='completed').count()
    })