from django.db import models
from django.urls import reverse


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
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, related_name='category', null=True, blank=True)
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