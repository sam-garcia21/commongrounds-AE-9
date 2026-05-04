from django.contrib import admin
from .models import Genre, Book, Profile, Bookmark, BookReview, Borrow

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'role',)
    search_fields = ('user__username', 'displaye_name',)
    list_filter = ('role',)

class GenreAdmin(admin.ModelAdmin):
    model = Genre 
    search_fields = ('name', )
    list_display = ('name', 'description', )

class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'author', )
    list_display = ('title', 'author', 'genre', 'publication_year', )
    list_filter = ('author', 'genre', 'publication_year', )

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book', 'profile',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'title', 'user_reviewer', 'anon_reviewer',)
    list_filter = ('book',)

class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'name', 'date_borrowed', 'date_return',)
    readonly_fields = ('date_return',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(BookReview, ReviewAdmin)
admin.site.register(Borrow, BorrowAdmin)