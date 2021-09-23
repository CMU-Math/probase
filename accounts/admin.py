from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.action(description='Make selected users active')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='Make selected users inactive')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'first_name',
        'last_name',
        'email',
        'is_writer',
        'is_solver',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'is_writer',
        'is_solver',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_writer',
                'is_solver',
                'is_staff',
                'is_active',
                'is_new',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_writer',
                'is_solver',
                'is_staff',
                'is_active',
                'is_new',
            )
        }),
    )
    search_fields = (
        'first_name',
        'last_name',
    )
    ordering = ('pk',)
    actions = (
        make_active,
        make_inactive,
    )

admin.site.register(User, CustomUserAdmin)

