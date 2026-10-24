from django.db import models
from users.models import User, Organization
from opportunities.models import Opportunity


class Application(models.Model):
    STATUS_CHOICES = (
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')
    applied_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('volunteer', 'opportunity')

    def _str_(self):
        return f"{self.volunteer.username} → {self.opportunity.title}"


class Participation(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='participations')
    hours_completed = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_participations')
    completion_date = models.DateField(blank=True, null=True)

    def _str_(self):
        return f"{self.volunteer.username} - {self.hours_completed}h"