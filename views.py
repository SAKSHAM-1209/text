from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import Banquet, Venue
from .forms import (
    SignUpForm, LoginForm, BanquetForm,
    ScheduleCallForm, ContactMessageForm
)

# ===== STATIC PAGES =====
def landing(request):
    banquets = None
    location = request.GET.get('location')
    guests = request.GET.get('guests')
    function_type = request.GET.get('function_type')

    if location or guests or function_type:
        banquets = Banquet.objects.all()
        if location:
            banquets = banquets.filter(location__icontains=location)
        if guests:
            try:
                guests_int = int(guests)
                banquets = banquets.filter(capacity__gte=guests_int)
            except ValueError:
                pass
        if function_type:
            banquets = banquets.filter(services=function_type)

    return render(request, 'landing.html', {'banquets': banquets})


def about(request):
    return render(request, 'about.html')


def banquet(request):
    banquets = Banquet.objects.all()
    return render(request, 'banquet.html', {'banquets': banquets})


# ===== SIGNUP =====
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # Optional Venue Info
            venue_name = request.POST.get('venue_name')
            venue_address = request.POST.get('venue_address')
            venue_capacity = request.POST.get('venue_capacity')
            venue_price = request.POST.get('venue_price')

            if venue_name and venue_address and venue_capacity and venue_price:
                try:
                    Venue.objects.create(
                        user=user,
                        name=venue_name,
                        address=venue_address,
                        capacity=int(venue_capacity),
                        price=float(venue_price)
                    )
                except Exception as e:
                    print('Venue creation error:', e)

            # Emails
            send_mail(
                "🎉 Welcome to FindMyBanquet!",
                f"Hello {user.first_name},\n\nThank you for registering with FindMyBanquet.\n\n– Team FindMyBanquet",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            send_mail(
                f"🆕 New User Registered: {user.get_full_name()}",
                f"Name: {user.get_full_name()}\nEmail: {user.email}",
                settings.EMAIL_HOST_USER,
                ['findmybanquetofficial@gmail.com'],
                fail_silently=False
            )

            login(request, user)
            messages.success(request, '✅ Account created successfully!')
            return redirect('landing')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


# ===== LOGIN =====
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, '✅ Logged in successfully!')
            return redirect(request.GET.get('next', 'landing'))
        else:
            messages.error(request, '⚠ Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# ===== LOGOUT =====
def logout_view(request):
    logout(request)
    messages.info(request, '✅ Logged out successfully.')
    return redirect('landing')


# ===== REGISTER BANQUET =====
@login_required
def register_banquet(request):
    if request.method == 'POST':
        form = BanquetForm(request.POST, request.FILES)
        if form.is_valid():
            banquet = form.save(commit=False)
            banquet.owner = request.user
            banquet.owner_name = request.user.get_full_name()
            banquet.save()

            send_mail(
                "🏛 Your Banquet Has Been Registered!",
                f"Hello {request.user.get_full_name()},\n\nYour banquet has been added successfully.\n\n– Team FindMyBanquet",
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False
            )

            messages.success(request, '✅ Banquet registered successfully!')
            return redirect('banquet')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BanquetForm()

    return render(request, 'register.html', {'form': form})


# ===== SCHEDULE CALL =====
def schedule_call(request):
    if request.method == 'POST':
        form = ScheduleCallForm(request.POST)
        if form.is_valid():
            call = form.save()

            send_mail(
                "📅 Your Call Has Been Scheduled!",
                f"Hello {call.name},\n\nYour call is scheduled on {call.date} at {call.time_slot}.\n\n– Team FindMyBanquet",
                settings.EMAIL_HOST_USER,
                [call.email],
                fail_silently=False
            )

            messages.success(request, '✅ Your call has been scheduled successfully!')
            return redirect('landing')
        else:
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ScheduleCallForm()

    return render(request, 'schedule-call.html', {'form': form})


# ===== CONTACT US (✅ FIXED HERE) =====
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()

            # EMAIL TO USER
            send_mail(
                "📩 Thanks for Contacting FindMyBanquet!",
                f"Hello {message.full_name},\n\n"
                f"Thank you for contacting FindMyBanquet. We’ll get back to you soon.\n\n"
                f"Your Message:\n{message.message}\n\n– Team FindMyBanquet",
                settings.EMAIL_HOST_USER,
                [message.email],
                fail_silently=False
            )

            # EMAIL TO ADMIN
            send_mail(
                f"📨 New Contact Message from {message.full_name}",
                f"Name: {message.full_name}\n"
                f"Email: {message.email}\n"
                f"Subject: {message.subject}\n\n"
                f"Message:\n{message.message}",
                settings.EMAIL_HOST_USER,
                ['findmybanquetofficial@gmail.com'],
                fail_silently=False
            )

            messages.success(request, '✅ Your message has been sent successfully!')
            return redirect('landing')
        else:
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})


# ===== TEST EMAIL =====
def test_email(request):
    try:
        send_mail(
            "📧 Local SMTP Test",
            "Hello Saksham! If you got this, SMTP is working locally ✅",
            settings.EMAIL_HOST_USER,
            ["saksham.shukla1209@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully from LOCAL server!")
    except Exception as e:
        return HttpResponse(f"❌ Error sending email: {e}")
