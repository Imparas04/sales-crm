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
    import json
    from django.db.models import Sum, Count
    from django.utils import timezone
    from .models import Customer, Lead, Sale, FollowUp, Product

    profile = getattr(request.user, "profile", None)

    # ---- KPI cards ----
    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()
    total_sales = Sale.objects.count()

    today = timezone.localdate()
    month_start = today.replace(day=1)
    monthly_sales = Sale.objects.filter(sale_date__gte=month_start)
    monthly_revenue = sum((s.total() for s in monthly_sales), 0) if monthly_sales.exists() else 0

    won_leads = Lead.objects.filter(status="won").count()
    conversion_rate = round((won_leads / total_leads * 100), 1) if total_leads else 0

    pending_followups = FollowUp.objects.filter(status="pending").count()

    # ---- Chart data ----
    # Lead status breakdown
    lead_status_qs = Lead.objects.values("status").annotate(count=Count("id"))
    lead_status_labels = [row["status"] for row in lead_status_qs]
    lead_status_counts = [row["count"] for row in lead_status_qs]

    # Sales by product (top 5 by revenue, computed in Python since total() incl. discount/gst is a method not a DB field)
    product_revenue = {}
    for sale in Sale.objects.prefetch_related("items__product"):
        for item in sale.items.all():
            product_revenue[item.product.name] = product_revenue.get(item.product.name, 0) + float(item.line_total())
    top_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
    product_labels = [p[0] for p in top_products]
    product_values = [p[1] for p in top_products]

    context = {
        "profile": profile,
        "total_customers": total_customers,
        "total_leads": total_leads,
        "total_sales": total_sales,
        "monthly_revenue": monthly_revenue,
        "conversion_rate": conversion_rate,
        "pending_followups": pending_followups,
        "lead_status_labels": json.dumps(lead_status_labels),
        "lead_status_counts": json.dumps(lead_status_counts),
        "product_labels": json.dumps(product_labels),
        "product_values": json.dumps(product_values),
    }
    return render(request, "dashboard.html", context)
