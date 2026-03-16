from django.urls import path
from . import views
urlpatterns = [
    path('library/', views.library_view, name='library' ),
    path('category/<slug:slug>/', views.category_books, name='category_books'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]

