from django.db import models
from users.models import Organization


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.name


class Opportunity(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='opportunities')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    hours = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=1)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    image = models.ImageField(upload_to='opportunities/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title