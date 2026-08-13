from django.urls import path
from . import views, views_customer, views_lead, views_product, views_followup, views_quotation, views_sale, views_ai, views_notification

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

    # Products
    path("products/", views_product.product_list, name="product_list"),
    path("products/add/", views_product.product_add, name="product_add"),
    path("products/<int:pk>/edit/", views_product.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views_product.product_delete, name="product_delete"),

    # Follow-ups
    path("followups/", views_followup.followup_dashboard, name="followup_dashboard"),
    path("followups/all/", views_followup.followup_list, name="followup_list"),
    path("followups/add/", views_followup.followup_add, name="followup_add"),
    path("followups/<int:pk>/edit/", views_followup.followup_edit, name="followup_edit"),
    path("followups/<int:pk>/delete/", views_followup.followup_delete, name="followup_delete"),
    path("followups/<int:pk>/complete/", views_followup.followup_mark_complete, name="followup_complete"),

    # Quotations
    path("quotations/", views_quotation.quotation_list, name="quotation_list"),
    path("quotations/add/", views_quotation.quotation_add, name="quotation_add"),
    path("quotations/<int:pk>/", views_quotation.quotation_detail, name="quotation_detail"),
    path("quotations/<int:pk>/edit/", views_quotation.quotation_edit, name="quotation_edit"),
    path("quotations/<int:pk>/delete/", views_quotation.quotation_delete, name="quotation_delete"),
    path("quotations/<int:pk>/pdf/", views_quotation.quotation_pdf, name="quotation_pdf"),
    path("quotations/<int:quotation_pk>/create-sale/", views_sale.sale_from_quotation, name="sale_from_quotation"),

    # Sales
    path("sales/", views_sale.sale_list, name="sale_list"),
    path("sales/add/", views_sale.sale_add, name="sale_add"),
    path("sales/<int:pk>/", views_sale.sale_detail, name="sale_detail"),
    path("sales/<int:pk>/delete/", views_sale.sale_delete, name="sale_delete"),

    # AI Module
    path("leads/<int:pk>/ai-score/", views_ai.ai_score_lead, name="ai_score_lead"),
    path("leads/<int:pk>/ai-followup/", views_ai.ai_followup_lead, name="ai_followup_lead"),
    path("customers/<int:pk>/ai-summary/", views_ai.ai_customer_summary, name="ai_customer_summary"),
    path("ai-sales-report/", views_ai.ai_sales_report, name="ai_sales_report"),

    # Notifications
    path("notifications/", views_notification.notification_list, name="notification_list"),
    path("notifications/<int:pk>/read/", views_notification.notification_mark_read, name="notification_mark_read"),
    path("notifications/mark-all-read/", views_notification.notification_mark_all_read, name="notification_mark_all_read"),
]
