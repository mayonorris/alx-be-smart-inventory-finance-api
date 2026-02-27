from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'

    email = models.EmailField(unique=True)
    role  = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN