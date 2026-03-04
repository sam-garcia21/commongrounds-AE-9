from django.contrib import admin
from .models import Genre, Book

# Register your models here.
class BookInline(admin.TabularInline):
    model = Book

class GenreAdmin(admin.ModelAdmin):
    model = Genre 
    inlines = [BookInline,]
    search_fields = ('name', )
    list_display = ('name', 'description', )

class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'author', )
    list_display = ('title', 'author', 'genre', 'publication_year')
    list_filter = ('author', 'genre', 'publication_year', )

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)