from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre, BookReview, Bookmark, Borrow
from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    contributed = []
    bookmarked = []
    reviewed = []
    if request.user.is_authenticated:
        profile = request.user.profile
        contributed = Book.objects.filter(contributor=profile)
        bookmarked = Book.objects.filter(bookmarks__profile=profile)
        reviewed = Book.objects.filter(reviews__user_reviewer=profile)

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
    book = get_object_or_404(Book, pk=pk)
    bookmarks_count = book.bookmarks.count()
    reviews = book.reviews.all()

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'bookmark' and request.user.is_authenticated:
            bookmark, created = Bookmark.objects.get_or_create(book=book, profile=request.user.profile)
            if not created:
                bookmark.delete()
        elif action == 'review':
            title = request.POST.get('title')
            comment = request.POST.get('comment')

            user_profile = request.user.profile if request.user.is_authenticated else None
            anon_name = request.POST.get('name', 'Anonymous')

            BookReview.objects.create(book=book, user_reviewer=user_profile, anon_reviewer=anon_name if not user_profile else "", title=title, comment=comment)

        return redirect('bookclub:book_detail', pk=book.pk)

    bookmarks_count = book.bookmarks.count()
    reviews = book.reviews.all()

    can_edit = False 
    if request.user.is_authenticated and book.contributor == request.user.profile:
        can_edit = True
    return render(request, "book_detail.html", {
        "book" : book,
        "bookmarks_count" : bookmarks_count,
        "reviews" : reviews,
        "can_edit" : can_edit,
    })

@login_required
def book_create(request):
    if request.user.profile.role != "Book Contributor":
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        synopsis = request.POST.get('synopsis')
        publication_year = request.POST.get('publication_year')
        genre_id = request.POST.get('genre')

        genre = get_object_or_404(Genre, id=genre_id)

        Book.objects.create(
            title=title,
            author=author,
            synopsis=synopsis,
            publication_year=publication_year,
            genre=genre,
            contributor=request.user.profile,
            is_available = True,
        )
        return redirect('bookclub:book_list')

    genres = Genre.objects.all().order_by('name')
    return render(request, "book_form.html", {"genres" : genres})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.contributor != request.user.profile:
        raise PermissionDenied

    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.synopsis = request.POST.get('synopsis')
        book.publication_year = request.POST.get('publication_year')

        book.is_available = 'is_available' in request.POST

        genre_id = request.POST.get('genre')
        book.genre = get_object_or_404(Genre, id=genre_id)

        book.save()
        return redirect('bookclub:book_detail', pk=book.pk)
    
    genres = Genre.objects.all()
    return render(request, "book_form.html", {
        "book" : book,
        "genres" : genres,
    })

def book_borrow(request, pk):
    book = get_object_or_404(Book, pk=pk)

    profile = None

    if request.user.is_authenticated and book.contributor == request.user.profile:
        return redirect('bookclub:book_detail', pk=book.pk)

    if request.method == "POST":
        borrower_name = request.POST.get('name')
        if request.user.is_authenticated:
            profile = request.user.profile
        else:
            None 
        Borrow.objects.create(
            book=book,
            borrower=profile,
            name=borrower_name,
            date_borrowed=date.today()
        )

        book.is_available = False
        book.save()

        return redirect('bookclub:book_detail', pk=book.pk)

    return render(request, 'book_borrow.html', {"book" : book})
