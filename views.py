from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Banquet, Venue
from .forms import (
    SignUpForm, LoginForm, BanquetForm, BanquetImageForm,
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

            # ✅ Optional Venue Info
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

            # ✅ Send Email to User & Admin
            subject_user = "🎉 Welcome to FindMyBanquet!"
            message_user = f"Hello {user.first_name},\n\nThank you for registering with FindMyBanquet. We're excited to have you!\n\n– Team FindMyBanquet"
            subject_admin = f"🆕 New User Registered: {user.get_full_name()}"
            message_admin = f"Name: {user.get_full_name()}\nEmail: {user.email}"

            send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, ['findmybanquetofficial@gmail.com'], fail_silently=False)

            login(request, user)
            messages.success(request, '✅ Account created successfully!')
            return redirect('landing')
        else:
            print('Signup errors:', form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


# ===== LOGIN =====
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '✅ Logged in successfully!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('landing')
        else:
            print('Login errors:', form.errors)
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

            # ✅ Send Email to User & Admin
            subject_user = "🏛 Your Banquet Has Been Registered!"
            message_user = f"Hello {request.user.get_full_name()},\n\nYour banquet '{banquet.name}' has been successfully added to FindMyBanquet.\n\n– Team FindMyBanquet"
            subject_admin = f"🆕 New Banquet Registered: {banquet.name}"
            message_admin = f"Owner: {request.user.get_full_name()}\nEmail: {request.user.email}\nBanquet: {banquet.name}\nLocation: {banquet.location}"

            send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [request.user.email], fail_silently=False)
            send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, ['findmybanquetofficial@gmail.com'], fail_silently=False)

            messages.success(request, '✅ Banquet registered successfully!')
            return redirect('banquet')
        else:
            print('Banquet form errors:', form.errors)
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

            # ✅ Send Email to User & Admin
            subject_user = "📅 Your Call Has Been Scheduled!"
            message_user = (
                f"Hello {call.name},\n\n"
                f"Thank you for scheduling a call with FindMyBanquet.\n"
                f"Here are your call details:\n\n"
                f"📍 Date: {call.date}\n"
                f"🕒 Time: {call.time_slot}\n"
                f"📞 Contact: {call.phone}\n\n"
                f"We’ll get in touch with you soon!\n\n– Team FindMyBanquet"
            )

            subject_admin = f"📞 New Call Scheduled by {call.name}"
            message_admin = (
                f"Name: {call.name}\n"
                f"Email: {call.email}\n"
                f"Phone: {call.phone}\n"
                f"Date: {call.date}\n"
                f"Time: {call.time_slot}\n"
                f"Message: {call.message}"
            )

            send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [call.email], fail_silently=False)
            send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, ['findmybanquetofficial@gmail.com'], fail_silently=False)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"✅ Your call has been scheduled for {call.date} at {call.time_slot}.",
                })
            messages.success(request, '✅ Your call has been scheduled successfully!')
            return redirect('landing')

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ScheduleCallForm()

    return render(request, 'schedule-call.html', {'form': form})


# ===== CONTACT US =====
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()

            # ✅ Send Email to User & Admin
            subject_user = "📩 Thanks for Contacting FindMyBanquet!"
            message_user = f"Hello {message.name},\n\nThank you for contacting FindMyBanquet! We'll get back to you soon.\n\nYour Message:\n{message.message}\n\n– Team FindMyBanquet"

            subject_admin = f"📨 New Contact Message from {message.name}"
            message_admin = f"Name: {message.name}\nEmail: {message.email}\nSubject: {message.subject}\n\nMessage:\n{message.message}"

            send_mail(subject_user, message_user, settings.EMAIL_HOST_USER, [message.email], fail_silently=False)
            send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, ['findmybanquetofficial@gmail.com'], fail_silently=False)

            messages.success(request, '✅ Your message has been sent successfully!')
            return redirect('landing')
        else:
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})
