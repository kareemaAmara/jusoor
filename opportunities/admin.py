from django.contrib import admin
from .models import Category, Opportunity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'category', 'location', 'start_date', 'status')
    list_filter = ('status', 'category', 'location')
    search_fields = ('title', 'description')