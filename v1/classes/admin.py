from django.contrib import admin
from classes.models import Course


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ["title", 'price', 'teacher', 'published']