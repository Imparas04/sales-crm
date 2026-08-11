from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection


def home(request):
    return render(request, "login.html")


def ping_db(request):
    """Quick sanity check: confirms Django <-> MySQL connection works."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    return JsonResponse({"db_status": "connected", "result": result})
