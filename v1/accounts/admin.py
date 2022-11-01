from django.contrib import admin
from accounts.models import User, Profile, Request

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "balance", "role", "token")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "phone_number", "passport_number")

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["user", "role", 'status', "attachment"]