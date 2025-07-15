from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils import check_email_deliverability

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address where you can receive verification emails.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'autocomplete': 'email'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styles to other fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def clean_email(self):
        """
        Validate that the email is not already in use and check for deliverability issues.
        """
        email = self.cleaned_data.get('email')
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email or reset your password.")
        
        # Check for common typos and deliverability issues
        is_deliverable, issues, _ = check_email_deliverability(email)
        if not is_deliverable and issues:
            # Add warnings but don't prevent registration
            for issue in issues:
                self.add_warning('email', issue)
        
        return email
    
    def add_warning(self, field, message):
        """
        Add a warning message to a field without preventing form validation.
        """
        if not hasattr(self, '_warnings'):
            self._warnings = {}
        
        if field not in self._warnings:
            self._warnings[field] = []
            
        self._warnings[field].append(message)
    
    def get_warnings(self, field):
        """
        Get warnings for a specific field.
        """
        if hasattr(self, '_warnings') and field in self._warnings:
            return self._warnings[field]
        return []

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # User won't be active until email is verified
        if commit:
            user.save()
        return user
