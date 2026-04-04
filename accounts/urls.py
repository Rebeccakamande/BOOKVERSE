from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register" ),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
