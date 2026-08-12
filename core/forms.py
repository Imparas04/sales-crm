from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Customer, Lead, Product, FollowUp, Quotation, QuotationItem, Sale, SaleItem


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name", "email", "phone", "company", "address",
            "city", "industry", "status", "assigned_employee",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "name", "company", "email", "phone", "source",
            "interested_product", "budget", "status", "priority",
            "assigned_employee", "expected_closing_date", "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
            "expected_closing_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock", "description", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            "customer", "lead", "date", "time", "type",
            "notes", "status", "assigned_employee",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        lead = cleaned_data.get("lead")
        if not customer and not lead:
            raise forms.ValidationError("Select either a Customer or a Lead for this follow-up.")
        if customer and lead:
            raise forms.ValidationError("Select only one: either a Customer or a Lead, not both.")
        return cleaned_data


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ["customer", "discount", "gst", "status"]


QuotationItemFormSet = forms.inlineformset_factory(
    Quotation,
    QuotationItem,
    fields=["product", "quantity", "price"],
    extra=1,
    can_delete=True,
)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "invoice_number", "customer", "quotation", "discount", "gst",
            "payment_status", "payment_method", "sales_employee",
        ]


SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    fields=["product", "quantity", "price"],
    extra=1,
    can_delete=True,
)
