from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('first_name', 'last_name', 'email', 'is_writer', 'is_solver', 'is_staff', 'is_active',)
    list_filter = ('is_writer', 'is_solver', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_writer', 'is_solver', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_writer', 'is_solver', 'is_staff', 'is_active')}),
    )
    search_fields = ('first_name', 'last_name')
    ordering = ('first_name',)

admin.site.register(User, UserAdmin)

