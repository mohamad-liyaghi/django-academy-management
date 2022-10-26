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
        return f"{self.user}"



