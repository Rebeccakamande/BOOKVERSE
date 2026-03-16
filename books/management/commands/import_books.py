import requests
from django.core.management.base import BaseCommand
from books.models import Book, Category
from django.conf import settings


class Command(BaseCommand):
    help = "Import books from Google Books API"

    GOOGLE_API_URL = "https://www.googleapis.com/books/v1/volumes"

    def fetch_books_from_google(self, query, max_results=25):
        # Replace spaces with '+' for safe URL
        query = query.replace(" ", "+")
        params = {
            "q": f"subject:{query}",
            "maxResults": max_results,
            "printType": "books",
            "key": settings.GOOGLE_BOOKS_API_KEY
        }

        try:
            response = requests.get(self.GOOGLE_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            if not items:
                self.stdout.write(f"No books returned for query: {query}")
            return items

        except requests.RequestException as e:
            self.stdout.write(f"Failed to fetch books for {query}: {str(e)}")
            return []

    def handle(self, *args, **options):
        categories_to_import = [
            "Programming",
            "Science Fiction",
            "Mystery",
            "Fantasy",
            "Romance",
        ]

        max_per_category = 25  # Max per API fetch (≤40)
        self.stdout.write("Starting import...\n")

        for category_name in categories_to_import:
            self.stdout.write(f"Processing category: {category_name}")

            books = self.fetch_books_from_google(category_name, max_results=max_per_category)
            self.stdout.write(f"Fetched {len(books)} books for {category_name}")

            for item in books:
                volume_info = item.get("volumeInfo", {})

                title = volume_info.get("title", "No Title")

                authors = volume_info.get("authors", ["Unknown"])
                author = ", ".join(authors)
                if len(author) > 255:
                    author = author[:250] + "..."

                description = volume_info.get("description", "")
                page_count = volume_info.get("pageCount")
                language = volume_info.get("language", "")
                published_date = volume_info.get("publishedDate", "")
                api_id = item.get("id")

                # Cover image: try higher quality
                image_links = volume_info.get("imageLinks", {})
                cover_image_url = image_links.get("thumbnail") or image_links.get("smallThumbnail")
                if cover_image_url:
                    cover_image_url = cover_image_url.replace("http://", "https://")
                    cover_image_url = cover_image_url.replace("zoom=1", "zoom=3")  # better quality

                # ISBN
                isbn_list = volume_info.get("industryIdentifiers", [])
                isbn = isbn_list[0].get("identifier")[:50] if isbn_list else None

                # Skip duplicates
                if Book.objects.filter(api_id=api_id).exists():
                    self.stdout.write(f"Book '{title}' already exists, skipping.")
                    continue

                # Save book
                book = Book.objects.create(
                    title=title,
                    author=author,
                    description=description,
                    page_count=page_count,
                    language=language,
                    published_date=published_date,
                    api_id=api_id,
                    cover_image_url=cover_image_url,
                    isbn=isbn,
                )

                # Create/get category
                category, _ = Category.objects.get_or_create(name=category_name)
                book.categories.add(category)

                self.stdout.write(f"Saved book: {title}")

            self.stdout.write(f"Finished category '{category_name}' with {len(books)} books.\n")

        self.stdout.write("Import completed successfully!")