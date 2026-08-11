from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import UserProfile


def ping_db(request):
    """Quick sanity check: confirms Django <-> MySQL connection works."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    return JsonResponse({"db_status": "connected", "result": result})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # create_user() hashes the password automatically (PBKDF2 by default)
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )
            UserProfile.objects.create(
                user=user,
                role=data["role"],
                phone=data.get("phone", ""),
            )
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Django creates the session here
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required(login_url="login")
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required(login_url="login")
def dashboard_view(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "dashboard.html", {"profile": profile})
