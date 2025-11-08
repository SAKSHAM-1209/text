# ======================= settings.py =======================

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ===== BASE DIR =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== LOAD .env =====
load_dotenv(os.path.join(BASE_DIR, '.env'))
# ===== SECURITY =====
SECRET_KEY = os.getenv('SECRET_KEY')

# ===== ENVIRONMENT & DEBUG =====
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()  # Default to local if not set
DEBUG = os.getenv('DEBUG', '1').lower() in ['1', 'true', 'yes']

# ===== ALLOWED HOSTS =====
# DEFAULT_ALLOWED_HOSTS = [
#     '127.0.0.1',
#     'localhost',
#     'find-banquet.onrender.com',
#     'findmybanquet.com',
#     'www.findmybanquet.com',
# ]

ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')]

# ===== CSRF TRUSTED ORIGINS =====
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://find-banquet.onrender.com',
    'https://findmybanquet.com',
    'https://www.findmybanquet.com',
]

# ===== INSTALLED APPS =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',  # your main app
]

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===== URLS & WSGI =====
ROOT_URLCONF = 'Banquet.urls'
WSGI_APPLICATION = 'Banquet.wsgi.application'

# ===== TEMPLATES =====
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===== DATABASE CONFIGURATION =====


db_url = os.getenv('DATABASE_URL')

if ENVIRONMENT in ['local', 'development']:
    DATABASES = {
        'default': dj_database_url.parse(db_url, conn_max_age=0, ssl_require=False)
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(db_url, conn_max_age=600, ssl_require=True)
    }



# ===== PASSWORD VALIDATION =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== INTERNATIONALIZATION =====
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ===== STATIC FILES =====
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===== MEDIA FILES =====
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===== DEFAULT PRIMARY KEY =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== SECURITY SETTINGS =====
# if ENVIRONMENT == 'production':
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     USE_X_FORWARDED_HOST = True
# else:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False

# ===== DEVELOPMENT SETTINGS =====
# if ENVIRONMENT in ['local', 'dev', 'development']:
#     # Rename cookies to prevent conflicts
#     SESSION_COOKIE_NAME = 'sessionid_dev'
#     CSRF_COOKIE_NAME = 'csrftoken_dev'

#     # Disable CSRF locally to avoid random 400 errors
#     MIDDLEWARE = [mw for mw in MIDDLEWARE if mw != 'django.middleware.csrf.CsrfViewMiddleware']

#     # Verbose logging for debugging
#     LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {'console': {'class': 'logging.StreamHandler'}},
#         'loggers': {
#             'django.request': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
#             'django.security': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
#         },
#     }

# ===== REDIRECT SETTINGS =====
APPEND_SLASH = True
