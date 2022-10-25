from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''Custom user model'''

    class Role(models.TextChoices):
        '''User Role'''
        SUPERUSER = ("su", "Superuser")
        ADMIN = ("ad", "Admin")
        TEACHER = ("t", "Teacher")
        STUDENT = ("s", "Student")


    username = None
    email = models.EmailField(max_length=200, unique=True)

    balance = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.STUDENT)

    token = models.IntegerField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        return self.username



    