import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Order
from book.models import Book


def is_librarian(user):
    return user.is_authenticated and getattr(user, "role", 0) == 1


def order_list(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if is_librarian(request.user):
        orders = Order.get_all()
        return render(request, "order/order_list.html", {"orders": orders})

    return redirect("my_orders")


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user)
    return render(request, "order/my_orders.html", {"orders": orders})


def order_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    books = Book.get_all()

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        plated_end_at = request.POST.get("plated_end_at")

        book = Book.get_by_id(book_id)

        if book is None:
            messages.error(request, "Book not found")
            return redirect("order_create")

        if not plated_end_at:
            plated_end_at = int(time.time()) + 14 * 24 * 60 * 60
        else:
            plated_end_at = int(plated_end_at)

        Order.create(
            user=request.user,
            book=book,
            plated_end_at=plated_end_at
        )

        return redirect("my_orders")

    return render(request, "order/order_create.html", {"books": books})


def order_close(request, order_id):
    if not is_librarian(request.user):
        return redirect("home")

    order = get_object_or_404(Order, id=order_id)
    order.update(end_at=int(time.time()))

    return redirect("order_list")