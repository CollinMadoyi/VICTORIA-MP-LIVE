from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # This imports YOUR custom User model

class CustomUserCreationForm(UserCreationForm):
    # We add the email field explicitly to make it required
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta(UserCreationForm.Meta):
        model = User
        # We include username and email in the form fields
        fields = ("username", "email")

    def clean_email(self):
        """Ensure the email is unique in our custom User table."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email