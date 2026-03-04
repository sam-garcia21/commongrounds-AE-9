from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

BookCategory = Genre 

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, related_name="books")
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookclub:book_detail', args=[str(self.pk)])