from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Book
from order.models import Order
from authentication.models import CustomUser


def is_librarian(user):
    return user.is_authenticated and getattr(user, "role", 0) == 1


def book_list(request):
    books = Book.get_all()

    title = request.GET.get("title")
    author = request.GET.get("author")

    if title:
        books = books.filter(name__icontains=title)

    if author:
        books = books.filter(
            Q(authors__name__icontains=author) |
            Q(authors__surname__icontains=author) |
            Q(authors__patronymic__icontains=author)
        ).distinct()

    return render(request, "book/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book/book_detail.html", {"book": book})


def books_by_user(request, user_id):
    if not is_librarian(request.user):
        return redirect("home")

    user = get_object_or_404(CustomUser, id=user_id)
    orders = Order.objects.filter(user=user)
    books = []

    for order in orders:
        if order.book and order.book not in books:
            books.append(order.book)

    return render(
        request,
        "book/books_by_user.html",
        {"books": books, "selected_user": user}
    )