from django.db import models
from books.models import Book
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    comment = models.TextField()
    rating = models.IntegerField(blank=True, null=True)

    approved = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_book_review'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
