from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User

class Course(models.Model):

    class Difficulty(models.TextChoices):
        '''Difficulty status'''

        BEGINNER = ("b", "Beginner")
        INTERMEDIATE = ("i", "Intermediate")
        ADVANCE = ("a", "Advance")


    title = models.CharField(max_length=220)
    description = models.TextField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")

    price = models.IntegerField(default=0, validators=[
            MaxValueValidator(5000),
            MinValueValidator(10)
        ])

    published = models.BooleanField(default=False)

    difficulty = models.CharField(max_length=1, choices=Difficulty.choices, 
                default=Difficulty.BEGINNER)

    time = models.FloatField(default=0, validators=[
            MinValueValidator(0.0)
        ])

    token = models.CharField(unique=True, max_length=15)
    
    def __str__(self) -> str:
        return self.title