from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from accounts.models import Profile

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="books")
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    contributor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="books")
    synopsis = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookclub:book_detail', args=[str(self.pk)])

class BookReview(models.Model):
    user_reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    anon_reviewer = models.CharField(max_length=255, default="Anonymous")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=255)
    comment = models.TextField()

class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookmarks')
    date_bookmarked = models.DateField(auto_now_add=True)

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_borrowed = models.DateField()
    date_return = models.DateField()

    def save(self, *args, **kwargs):
        if not self.date_return and self.date_borrowed:
            self.date_return = self.date_borrowed + timedelta(days=14)
        super().save(*args, **kwargs)