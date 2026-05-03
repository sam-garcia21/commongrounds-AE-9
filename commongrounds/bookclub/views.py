from django.shortcuts import render
from .models import Book, Genre, BookReview, Bookmark, Borrow
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    contributed = []
    bookmarked = []
    reviewed = []
    if request.user.is_authenticated:
        profile = request.user.profile
        contributed = Book.objects.filter(contributor=profile)
        bookmarked = Books.objects.filter(bookmarks__profile=profile)
        reviewed = Books.objects.filter(reviews__user_reviewer=profile)

        books = books.exclude(contributor=profile)
        books = books.exclude(bookmarks__profile=profile)
        books = books.exclude(reviews__user_reviewer=profile)
    return render(request, "book_list.html", {
        "books" : books,
        "contributed" : contributed,
        "bookmarked" : bookmarked,
        "reviewed" : reviewed,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    bookmarks_count = book.bookmars.count()
    reviews = book.reviews.all()

    can_edit = False 
    if request.user.is_authenticated and book.contributor == request.user.profile:
        can_edit = True
    return render(request, "book_detail.html", {
        "book" : book,
        "bookmarks_count" : bookmarks_count
        "reviews" : reviews,
        "can_edit" : can_edit
    })

@login_required
def book_create(request):
    if request.user.profile.role != "Book Contributor":
        return render(request, "403.html")

    return render(request, "book_form.html")