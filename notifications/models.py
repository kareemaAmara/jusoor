from django.db import models
from users.models import User


class Notification(models.Model):
    TYPE_CHOICES = (
        ('application_status', 'Application Status'),
        ('new_opportunity', 'New Opportunity'),
        ('reminder', 'Reminder'),
        ('system', 'System'),
        ('message', 'Message'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return f"{self.user.username} - {self.title}"


class Report(models.Model):
    REPORT_TYPES = (
        ('volunteers', 'Volunteers'),
        ('hours', 'Hours'),
        ('opportunities', 'Opportunities'),
        ('organizations', 'Organizations'),
    )

    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    date_range = models.CharField(max_length=100, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.report_type} - {self.created_at.date()}"