from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    OPERATOR = 'operator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (OPERATOR, 'Operator'),
        (USER, 'User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return f"{self.username} ({self.role})"
