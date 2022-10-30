from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

import uuid

from .validators import validate_file_size



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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        return self.email



class Profile(models.Model):
    '''User profile model'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    picture = models.ImageField(upload_to="users/pictures", 
                                validators=[validate_file_size])

    age = models.SmallIntegerField(default=1, validators=[
            MaxValueValidator(60),
            MinValueValidator(10)
        ])
    
    phone_regex = RegexValidator(regex="\(?\d{3}\)?-? *\d{3}-? *-?\d{4}", 
                                message="Phone number format must be like: (XXX) XXX XXXX")
                                
    phone_number = models.CharField(max_length=15, validators=[phone_regex])

    address = models.CharField(max_length=300)

    passport_number = models.CharField(max_length=10)


    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class Request(models.Model):
    '''A model for requesting to becode teacher or admin'''

    class Role(models.TextChoices):
        ''''''
        ADMIN = ("a", "Admin")
        TEACHER = ("t", "Teacher")
    
    class Status(models.TextChoices):
        '''Request Status'''

        PENDING = ("p", "pending")
        ACCEPTED = ("a", "Accepted")
        REJECTED = ("r", "Rejected")
        BLOCKED = ("b", "Blocked")


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.TEACHER)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)

    attachment = models.FileField(upload_to="users/requests", 
                                validators=[validate_file_size], blank=True, null=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)


    def __str__(self) -> str:
        return str(self.id)
