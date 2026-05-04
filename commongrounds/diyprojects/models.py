from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Profile


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'projectcategory'
        verbose_name_plural = 'project categories'


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, related_name='project', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='project', null=True, blank=True)
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('diyprojects:diyprojects_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'project'
        verbose_name_plural = 'project'


class Favorite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_favorited = models.DateTimeField(auto_now_add=True)
    STATUS = ((0, 'Backlog'), (1, 'To-Do'), (2, 'Done'))
    project_status = models.SmallIntegerField(choices=STATUS, default=0)

class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

