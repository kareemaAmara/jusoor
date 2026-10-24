from django.contrib import admin
from .models import Application, Participation


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'status', 'applied_date')
    list_filter = ('status',)
    search_fields = ('volunteer_username', 'opportunity_title')


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'hours_completed', 'verified', 'completion_date')
    list_filter = ('verified',)
    search_fields = ('volunteer_username', 'opportunity_title')