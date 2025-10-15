from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Banquet, BanquetImage, ScheduleCall, ContactMessage
from .constants import KANPUR_AREAS  # Location filter

# ===== SIGNUP FORM =====
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )

    # ===== Owner Fields =====
    venue_name = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Banquet / Venue Name'})
    )
    venue_address = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Venue Address'})
    )
    venue_capacity = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Capacity'})
    )
    venue_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price (INR)'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
            'venue_name', 'venue_address', 'venue_capacity', 'venue_price'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}),
        }

# ===== LOGIN FORM =====
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )
# ===== BANQUET FORM =====
class BanquetForm(forms.ModelForm):
    class Meta:
        model = Banquet
        fields = ['banquet_name', 'email', 'phone', 'capacity', 'location', 'google_link']
        widgets = {
            'banquet_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Banquet Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Capacity'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location'}),
            'google_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Google My Business Page Link'}),
        }


# ===== SCHEDULE CALL FORM =====
REASON_CHOICES = [
    ('', 'Select Reason'),
    ('Consultation', 'Consultation'),
    ('Support', 'Support'),
    ('Partnership', 'Partnership'),
    ('Other', 'Other'),
]

class ScheduleCallForm(forms.ModelForm):
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'reason'})
    )

    class Meta:
        model = ScheduleCall
        fields = ['name', 'email', 'phone', 'date', 'time_slot', 'reason', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time_slot': forms.Select(attrs={'class': 'form-input', 'id': 'timeSlot'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Additional Notes (optional)'}),
        }

# ===== CONTACT MESSAGE FORM =====
class ContactMessageForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('', 'Select a subject *'),
        ('Booking', 'Booking Inquiry'),
        ('Partnership', 'Venue Partnership'),
        ('Support', 'Technical Support'),
        ('General', 'General Inquiry'),
        ('Feedback', 'Feedback'),
        ('Other', 'Other'),
    ]

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'}),
        required=True
    )

    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name *'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email *'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Message * (max 500 characters)',
                'rows': 4,
                'maxlength': 500
            }),
        }
