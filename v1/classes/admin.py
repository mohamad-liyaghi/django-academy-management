from django.contrib import admin
from classes.models import Course, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", 'price', 'teacher', 'published']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "amount", "date"]