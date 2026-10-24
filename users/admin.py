from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone', 'profile_image', 'skills')}),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'user', 'verified')
    list_filter = ('verified',)
    search_fields = ('org_name',)