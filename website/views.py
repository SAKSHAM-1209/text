from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Banquet, BanquetImage
from .forms import (
    SignUpForm,
    LoginForm,
    BanquetForm,
    ScheduleCallForm,
    ContactMessageForm
)
from .constants import KANPUR_AREAS


# ==============================
# 🏠 LANDING PAGE
# ==============================
def landing(request):
    banquets = Banquet.objects.all()
    area = request.GET.get('area')
    guests = request.GET.get('guests')

    if area:
        banquets = banquets.filter(location__iexact=area)
    if guests:
        try:
            guests_int = int(guests)
            banquets = banquets.filter(capacity__gte=guests_int)
        except ValueError:
            pass

    context = {
        'banquets': banquets,
        'KANPUR_AREAS': KANPUR_AREAS,
        'request': request,
    }
    return render(request, 'landing.html', context)


# ==============================
# ℹ️ ABOUT PAGE
# ==============================
def about(request):
    return render(request, 'about.html')


# ==============================
# 🏨 BANQUET PAGE
# ==============================
def banquet(request):
    banquets = Banquet.objects.all()
    return render(request, 'banquet.html', {'banquets': banquets})


# ==============================
# 🧾 SIGNUP
# ==============================
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '✅ Account created successfully!')

            # Optional banquet creation if venue details are provided
            venue_name = request.POST.get('venue_name')
            venue_address = request.POST.get('venue_address')
            venue_capacity = request.POST.get('venue_capacity')
            venue_price = request.POST.get('venue_price')

            if venue_name and venue_address and venue_capacity and venue_price:
                try:
                    Banquet.objects.create(
                        owner_name=user.get_full_name() or user.username,
                        banquet_name=venue_name,
                        email=user.email,
                        phone="",
                        capacity=int(venue_capacity),
                        location=venue_address,
                        google_link="",
                        services=""
                    )
                    messages.success(request, '✅ Your banquet has been registered successfully!')
                except Exception as e:
                    print("Banquet creation error:", e)
                    messages.error(request, "⚠ Error saving your banquet. Please try again.")

            return redirect('landing')
        else:
            print("Signup form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


# ==============================
# 🔑 LOGIN
# ==============================
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '✅ Logged in successfully!')
            return redirect('landing')
        else:
            messages.error(request, '⚠ Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# ==============================
# 🚪 LOGOUT
# ==============================
def logout_view(request):
    logout(request)
    messages.info(request, '👋 Logged out successfully.')
    return redirect('landing')


# ==============================
# 🏛️ REGISTER BANQUET
# ==============================
@login_required(login_url='login')
def register_banquet(request):
    if request.method == 'POST':
        form = BanquetForm(request.POST)
        files = request.FILES.getlist('image')

        if form.is_valid():
            banquet = form.save(commit=False)
            banquet.owner = request.user
            banquet.owner_name = request.user.get_full_name() or request.user.username
            banquet.save()

            for f in files:
                BanquetImage.objects.create(banquet=banquet, image=f)

            messages.success(request, '✅ Banquet registered successfully with images!')
            return redirect('landing')
        else:
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = BanquetForm()

    return render(request, 'register.html', {'form': form})


# ==============================
# 📞 SCHEDULE CALL
# ==============================
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
            messages.success(request, '✅ Your call has been scheduled successfully!')
            return redirect('landing')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ScheduleCallForm()
    return render(request, 'schedule-call.html', {'form': form})


# ==============================
# 📬 CONTACT US (with Email)
# ==============================
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            try:
                # --- USER EMAIL ---
                subject_user = "📩 Thanks for contacting FindMyBanquet!"
                body_user = (
                    f"Hello {message.name},\n\n"
                    "We’ve received your message and will reach out soon.\n\n"
                    "Your Message:\n"
                    f"{message.message}\n\n"
                    "– Team FindMyBanquet"
                )

                # --- ADMIN EMAIL ---
                subject_admin = f"📨 New Contact from {message.name}"
                body_admin = (
                    f"Name: {message.name}\n"
                    f"Email: {message.email}\n"
                    f"Subject: {message.subject}\n\n"
                    f"Message:\n{message.message}"
                )

                # Send to user
                send_mail(
                    subject_user,
                    body_user,
                    settings.EMAIL_HOST_USER,
                    [message.email],
                    fail_silently=False,
                )

                # Send to admin
                send_mail(
                    subject_admin,
                    body_admin,
                    settings.EMAIL_HOST_USER,
                    ['findmybanquetofficial@gmail.com'],
                    fail_silently=False,
                )

                messages.success(request, '✅ Your message has been sent successfully!')
                return redirect('landing')

            except Exception as e:
                import traceback
                print("❌ Email sending error:", traceback.format_exc())
                messages.error(request, '⚠ Message saved, but email could not be sent.')
                return redirect('landing')

        else:
            messages.error(request, '⚠ Please correct the errors below.')
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})


# ==============================
# ✉ TEST EMAIL (For SMTP check)
# ==============================
def test_email(request):
    try:
        send_mail(
            subject="🎯 Test Email from Django (FindMyBanquet)",
            message="Hello Saksham! ✅ Your email setup is working perfectly.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["saksham.shukla1209@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully! Check your inbox.")
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        return HttpResponse(f"❌ Email failed:<br><pre>{error_message}</pre>")
