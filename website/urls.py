from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('banquet/', views.banquet, name='banquet'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-banquet/', views.register_banquet, name='register_banquet'),
    path('schedule-call/', views.schedule_call, name='schedule_call'),
    path('contact/', views.contact_us, name='contact'),

    # ✅ Test email URL
    path('test-email/', views.test_email, name='test_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
