from django.contrib import admin
from classes.models import Course, Payment, Session, Broadcast


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", 'price', 'teacher', 'published']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "amount", "date"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["number", "course", "time"]

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["course", "title", "date", "token"]