from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Information', {'fields': ('role', 'phone', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile Information', {'fields': ('role', 'phone', 'profile_pic')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
