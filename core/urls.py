from django.urls import path
from . import views, views_customer, views_lead

urlpatterns = [
    # Auth
    path("", views.login_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("ping-db/", views.ping_db, name="ping_db"),

    # Customers
    path("customers/", views_customer.customer_list, name="customer_list"),
    path("customers/add/", views_customer.customer_add, name="customer_add"),
    path("customers/<int:pk>/", views_customer.customer_view, name="customer_detail"),
    path("customers/<int:pk>/edit/", views_customer.customer_edit, name="customer_edit"),
    path("customers/<int:pk>/delete/", views_customer.customer_delete, name="customer_delete"),

    # Leads
    path("leads/", views_lead.lead_list, name="lead_list"),
    path("leads/add/", views_lead.lead_add, name="lead_add"),
    path("leads/<int:pk>/", views_lead.lead_view, name="lead_detail"),
    path("leads/<int:pk>/edit/", views_lead.lead_edit, name="lead_edit"),
    path("leads/<int:pk>/delete/", views_lead.lead_delete, name="lead_delete"),
    path("leads/<int:pk>/convert/", views_lead.lead_convert_to_customer, name="lead_convert"),
]
