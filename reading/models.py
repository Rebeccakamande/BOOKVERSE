from django.db import models
from books.models import Book
from django.db import models
from django.conf import settings


class ReadingProgress(models.Model):

    class ReadingStatus(models.TextChoices):
        TO_BE_READ = 'to_be_read', 'To Be Read'
        READING = 'reading', 'Currently Reading'
        COMPLETED = 'completed', 'Finished'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reading_progress'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reading_progress'
    )

    current_page = models.IntegerField(default=1)
    percentage = models.IntegerField(default=0)  # 0–100

    status = models.CharField(
        max_length=20,
        choices=ReadingStatus.choices,
        default=ReadingStatus.TO_BE_READ
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_book_progress'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
