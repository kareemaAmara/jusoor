from django.contrib import admin
from .models import Notification, Message, Report


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'title')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_read', 'sent_at')
    list_filter = ('is_read',)
    search_fields = ('sender_username', 'receiver_username')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'generated_by', 'created_at')
    list_filter = ('report_type',)