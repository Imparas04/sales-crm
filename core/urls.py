from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ping-db/", views.ping_db, name="ping_db"),
]
