from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # password hashed automatically

            # Save extra basic user info
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # ✅ Handle optional owner fields safely
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

            # Auto login after signup
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



@login_required
def register_banquet(request):
    if request.method == 'POST':
        form = BanquetForm(request.POST, request.FILES)
        if form.is_valid():
            banquet = form.save(commit=False)
            # set owner (required FK) and owner_name from logged-in user
            banquet.owner = request.user
            banquet.owner_name = request.user.get_full_name()
            banquet.save()
            messages.success(request, '✅ Banquet registered successfully!')
            return redirect('banquet')
        else:
            print('Banquet form errors:', form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BanquetForm()

    return render(request, 'register.html', {'form': form})

# ===== SCHEDULE CALL (AJAX-compatible) =====
def schedule_call(request):
    if request.method == 'POST':
        form = ScheduleCallForm(request.POST)
        if form.is_valid():
            call = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"✅ Your call has been scheduled for {call.date} at {call.time_slot}."
                })
            messages.success(request, 'Your call has been scheduled!')
            return redirect('landing')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ScheduleCallForm()
    return render(request, 'schedule-call.html', {'form': form})

# ===== CONTACT US =====
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('landing')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})
