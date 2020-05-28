from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name', 'email', 'is_writer', 'is_solver', 'is_staff', 'is_active',)
    list_filter = ('is_writer', 'is_solver', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_writer', 'is_solver', 'is_staff', 'is_active', 'is_new')}),
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_writer', 'is_solver', 'is_staff', 'is_active', 'is_new')}),
    )
    search_fields = ('first_name', 'last_name')
    ordering = ('pk',)

admin.site.register(User, CustomUserAdmin)

