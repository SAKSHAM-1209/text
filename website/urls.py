# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ===== Landing / Home page =====
    path('', views.landing, name='landing'),

    # ===== Static Pages =====
    path('about/', views.about, name='about'),
    path('banquet/', views.banquet, name='banquet'),

    # ===== Authentication =====
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ===== Banquet Registration (with multiple images) =====
    path('register-banquet/', views.register_banquet, name='register_banquet'),

    # ===== Schedule a Call =====
    path('schedule-call/', views.schedule_call, name='schedule_call'),

    # ===== Contact Form =====
    path('contact/', views.contact_us, name='contact'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
