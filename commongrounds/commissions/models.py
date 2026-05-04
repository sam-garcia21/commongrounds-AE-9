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
    OPEN = 0
    FULL = 1
    COMPLETED = 2
    DISCONTINUED = 3
    STATUS_CHOICES = {
        OPEN: "Open",
        FULL: "Full",
        COMPLETED: "Completed",
        DISCONTINUED: "Discontinued",
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
        null=True
    )
    people_required = models.IntegerField()
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.commission_type})'

    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_on']


class Job(models.Model):
    OPEN = 0
    FULL = 1
    STATUS_CHOICES = {
        OPEN: "Open",
        FULL: "Full",
    }
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs',
        null=True
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=OPEN
    )

    def isFull(self):
        accepted_applications = JobApplication.objects.filter(
            job=self).filter(status=JobApplication.ACCEPTED).count()
        return self.manpower_required <= accepted_applications

    def getOpenManpower(self):
        return self.manpower_required - JobApplication.objects.filter(
            job=self).filter(status=JobApplication.ACCEPTED).count()

    def __str__(self):
        return f'{self.commission.title} - {self.role}'

    class Meta:
        ordering = ['status', '-manpower_required', 'role']


class JobApplication(models.Model):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    STATUS_CHOICES = {
        PENDING: "Pending",
        ACCEPTED: "Accepted",
        REJECTED: "Rejected",
    }
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant.display_name} - {self.job.commission} ({self.job.role})'

    class Meta:
        ordering = ['status', '-applied_on']
