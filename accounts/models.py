from django.db import models
from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    is_blocked = models.BooleanField(default=False)

    full_name = models.CharField(max_length=150, blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username