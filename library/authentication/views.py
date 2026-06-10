from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import CustomUser


def home(request):
    return render(request, "authentication/home.html")


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name = request.POST.get("middle_name")
        role_value = request.POST.get("role", "0")

        if CustomUser.get_by_email(email):
            messages.error(request, "User with this email already exists")
            return redirect("register")

        user = CustomUser.create(
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

        if role_value in ["1", "admin", "librarian"]:
            user.role = 1
        else:
            user.role = 0

        user.is_active = True
        user.save()

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("home")

    return render(request, "authentication/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = CustomUser.get_by_email(email)

        if user and user.check_password(password):
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("home")

        messages.error(request, "Invalid email or password")
        return redirect("login")

    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def user_list(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return redirect("home")

    users = CustomUser.get_all()
    return render(request, "authentication/user_list.html", {"users": users})


def user_detail(request, user_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return redirect("home")

    user_obj = CustomUser.get_by_id(user_id)

    if user_obj is None:
        return redirect("user_list")

    return render(request, "authentication/user_detail.html", {"user_obj": user_obj})