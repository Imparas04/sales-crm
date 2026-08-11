from django.contrib import admin
from .models import (
    UserProfile, Customer, Lead, FollowUp, Product,
    Quotation, QuotationItem, Sale, SaleItem, Notification, AILog
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "company", "city", "status", "assigned_employee")
    list_filter = ("status", "city")
    search_fields = ("name", "phone", "email", "company")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "priority", "budget", "assigned_employee", "ai_score")
    list_filter = ("status", "priority")
    search_fields = ("name", "phone", "email", "company")


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "type", "status", "customer", "lead", "assigned_employee")
    list_filter = ("status", "type", "date")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "status")
    list_filter = ("status", "category")


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "quotation_date", "total")
    list_filter = ("status",)
    inlines = [QuotationItemInline]


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer", "payment_status", "sale_date", "total")
    list_filter = ("payment_status", "payment_method")
    inlines = [SaleItemInline]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    list_filter = ("is_read",)


@admin.register(AILog)
class AILogAdmin(admin.ModelAdmin):
    list_display = ("feature", "related_lead", "related_customer", "created_at")
    list_filter = ("feature",)
