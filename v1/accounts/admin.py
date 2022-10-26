from django.contrib import admin
from accounts.models import User, Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "balance", "role", "token")

admin.site.register(Profile)