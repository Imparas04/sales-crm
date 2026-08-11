from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Customer, Lead


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
