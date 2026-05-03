from django.db import models
from django.urls import reverse

from accounts.models import Profile

class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Commission(models.Model):
    OPEN = 'open'
    FULL = 'full'
    STATUS_CHOICES = {
        OPEN: "Open",
        FULL: "Full",
    }
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        related_name='commissions',
        null=True
    )
    maker = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='commisions',
    )
    people_required = models.IntegerField()
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.commission_type})'

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_on']
