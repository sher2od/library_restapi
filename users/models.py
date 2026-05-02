from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
        LIBRARIAN = 'librarian', 'Librarian'
        CLIENT = 'client', 'Client'

    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Phone number must be entered in the format: '+998XXXXXXXXX'."
    )
    
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, null=True, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    # library.Branch hali yaratilmagan, string reference + null=True
    branch = models.ForeignKey(
        'library.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
