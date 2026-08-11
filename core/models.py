from django.db import models
from django.contrib.auth.models import User


# ----------------------------------------------------------------------
# 1. USER PROFILE (extends Django's built-in User with role + extra info)
# ----------------------------------------------------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("sales_executive", "Sales Executive"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales_executive")
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ----------------------------------------------------------------------
# 2. CUSTOMER
# ----------------------------------------------------------------------
class Customer(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    assigned_employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="customers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------
# 3. LEAD
# ----------------------------------------------------------------------
class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal_sent", "Proposal Sent"),
        ("negotiation", "Negotiation"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    source = models.CharField(max_length=100, blank=True)  # e.g. website, referral, cold call
    interested_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    assigned_employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    expected_closing_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # AI Lead Scoring (Day 25) will fill these
    ai_score = models.IntegerField(null=True, blank=True)
    ai_recommendation = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"


# ----------------------------------------------------------------------
# 4. FOLLOW-UP
# ----------------------------------------------------------------------
class FollowUp(models.Model):
    TYPE_CHOICES = [
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("whatsapp", "WhatsApp"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="followups"
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=True, related_name="followups"
    )
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="call")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    assigned_employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="followups"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.customer or self.lead
        return f"{self.type} with {target} on {self.date}"


# ----------------------------------------------------------------------
# 5. PRODUCT
# ----------------------------------------------------------------------
class Product(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------
# 6. QUOTATION + QUOTATION ITEMS
# ----------------------------------------------------------------------
class Quotation(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotations")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotations"
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=18)      # percentage
    quotation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def subtotal(self):
        return sum(item.line_total() for item in self.items.all())

    def total(self):
        sub = self.subtotal()
        after_discount = sub - (sub * self.discount / 100)
        after_gst = after_discount + (after_discount * self.gst / 100)
        return round(after_gst, 2)

    def __str__(self):
        return f"Quotation #{self.id} - {self.customer.name}"


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)  # snapshot of price at quote time

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# ----------------------------------------------------------------------
# 7. SALE + SALE ITEMS
# ----------------------------------------------------------------------
class Sale(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("partial", "Partial"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank_transfer", "Bank Transfer"),
        ("card", "Card"),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    quotation = models.ForeignKey(
        Quotation, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales"
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cash")
    sales_employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales"
    )
    sale_date = models.DateField(auto_now_add=True)

    def subtotal(self):
        return sum(item.line_total() for item in self.items.all())

    def total(self):
        sub = self.subtotal()
        after_discount = sub - (sub * self.discount / 100)
        after_gst = after_discount + (after_discount * self.gst / 100)
        return round(after_gst, 2)

    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer.name}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)  # snapshot of price at sale time

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# ----------------------------------------------------------------------
# 8. NOTIFICATIONS
# ----------------------------------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"


# ----------------------------------------------------------------------
# 9. AI LOGS (stores every AI feature call - lead scoring, summaries, etc.)
# ----------------------------------------------------------------------
class AILog(models.Model):
    FEATURE_CHOICES = [
        ("lead_scoring", "Lead Scoring"),
        ("followup_generator", "Follow-up Generator"),
        ("customer_summary", "Customer Summary"),
        ("sales_report", "Sales Report"),
    ]

    feature = models.CharField(max_length=30, choices=FEATURE_CHOICES)
    related_lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="ai_logs"
    )
    related_customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="ai_logs"
    )
    input_summary = models.TextField(blank=True)
    ai_output = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feature} @ {self.created_at:%Y-%m-%d %H:%M}"
