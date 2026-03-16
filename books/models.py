from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True,null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Core Info
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Categories
    categories = models.ManyToManyField(Category, related_name='books', blank=True)

    # PDF File (for embedded viewer reading)
    file = models.FileField(upload_to='book_files/', blank=True, null=True)

    # Cover Handling (API or Manual)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True)

    # Metadata (usually filled from API)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    api_id = models.CharField(max_length=100, blank=True, null=True)

    # Ownership
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Visibility
    is_published = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_cover(self):
        """
        Returns the correct cover image.
        Manual upload overrides API cover.
        """
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']