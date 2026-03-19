from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update/<int:book_id>/<str:status>/', views.update_reading_status, name='update_reading_status'),
    path('read/<int:book_id>/', views.read_book, name='read_book'),
     path('save-progress/<int:book_id>/', views.save_progress, name='save_progress'),
     path('dashboard/progress-api/', views.dashboard_progress_api, name='dashboard_progress_api'),
]