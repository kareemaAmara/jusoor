from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('organization', 'Organization'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.username} ({self.role})"


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    org_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def _str_(self):
        return self.org_name