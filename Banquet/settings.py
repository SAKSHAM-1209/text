'''from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# ===== LOAD .env =====
load_dotenv()

# ===== BASE DIR =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== SECURITY =====
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-secret-key')
DEBUG = os.getenv('ENVIRONMENT', 'local').lower() == 'local'

# ===== ENVIRONMENT =====
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()

# ===== HOSTS =====
DEFAULT_ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'find-my-banquet-6wqy.onrender.com',  # Render URL
    'findmybanquet.com',
    'www.findmybanquet.com',
]

# Allow overriding ALLOWED_HOSTS via environment variable (comma-separated)
env_allowed = os.getenv('ALLOWED_HOSTS')
if env_allowed:
    ALLOWED_HOSTS = [h.strip() for h in env_allowed.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = DEFAULT_ALLOWED_HOSTS

# CSRF trusted origins (allow setting via env or default to known production hosts)
env_csrf = os.getenv('CSRF_TRUSTED_ORIGINS')
if env_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in env_csrf.split(',') if u.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ('127.0.0.1', 'localhost')]

# ===== INSTALLED APPS =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
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

ROOT_URLCONF = 'Banquet.urls'

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

WSGI_APPLICATION = 'Banquet.wsgi.application'

# ===== DATABASE CONFIGURATION (Supabase PostgreSQL with local SQLite fallback) =====
# Expect DATABASE_URL in the form provided by Supabase, e.g.
# postgres://USER:PASSWORD@HOST:PORT/DB
db_url = os.getenv('DATABASE_URL')
use_database_url = os.getenv('USE_DATABASE_URL', '0') == '1'

# In local/dev, default to SQLite even if DATABASE_URL exists, unless explicitly forced
if ENVIRONMENT in ['local', 'dev', 'development'] and not use_database_url:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Ensure SSL is required outside local envs
    ssl_require = ENVIRONMENT not in ['local', 'dev', 'development']
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=ssl_require,
        )
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

# ===== DEFAULT PRIMARY KEY FIELD TYPE =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== SECURITY SETTINGS =====
# Enable secure HTTPS-only settings when running in production
if ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # When running behind a proxy (Render, Heroku, etc.) set the header
    # that tells Django the request was originally HTTPS. Render sets
    # 'X-Forwarded-Proto' so configure Django to respect it.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
'''

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# ===== LOAD .env =====
load_dotenv()

# ===== BASE DIR =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== SECURITY =====
# Use a strong default key for local/dev so checks don't error; override via env in prod
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'dev-only-please-override-in-prod-1a2b3c4d5e6f7g8h9i0jKLMNOPQRSTUVWXyz1234567890abcdef',
)

# ===== ENVIRONMENT & DEBUG =====
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()
DEBUG = os.getenv('DEBUG', '0') == '1' if ENVIRONMENT != 'local' else True

# Enforce strong SECRET_KEY only in production
# Note: In production, ensure SECRET_KEY is set via environment to a unique, random value

# ===== HOSTS =====
# Open hosts universally to resolve BadRequest 400 due to host header during testing
DEFAULT_ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'find-banquet.onrender.com',
    'findmybanquet.com',
    'www.findmybanquet.com',
]
env_allowed = os.getenv('ALLOWED_HOSTS')
ALLOWED_HOSTS = ['*'] if not env_allowed else [h.strip() for h in env_allowed.split(',')]

# ===== CSRF Trusted Origins =====
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
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
    'website',
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

ROOT_URLCONF = 'Banquet.urls'

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

WSGI_APPLICATION = 'Banquet.wsgi.application'

# ===== DATABASE CONFIGURATION =====
"""db_url = os.getenv('DATABASE_URL', 'postgresql://saksham:ZJLpdBms1UCsI6pX0yVwq4cJUDZKUIY0@dpg-d3ilrqbe5dus7398i240-a/findmybanquet_db_f8pz')
use_database_url = os.getenv('USE_DATABASE_URL', '0') == '1'

if ENVIRONMENT in ['local', 'dev', 'development'] and not use_database_url:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=(ENVIRONMENT == 'production'),
        )
    }"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'DATABASE_URL':'postgresql://saksham:ZJLpdBms1UCsI6pX0yVwq4cJUDZKUIY0@dpg-d3ilrqbe5dus7398i240-a/findmybanquet_db_f8pz',
        'NAME': 'findmybanquet-db',
        'USER': 'saksham',
        'PASSWORD': 'ZJLpdBms1UCsI6pX0yVwq4cJUDZKUIY0',
        'HOST': 'localhost',
        'PORT': '5432',
    }
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

# ===== DEFAULT PRIMARY KEY FIELD TYPE =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ensure trailing slashes are redirected (helps avoid some 400s on odd paths)
APPEND_SLASH = True

# ===== SECURITY SETTINGS FOR PRODUCTION =====
if ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# In local/dev, rotate cookie names to avoid issues with stale/corrupt cookies causing 400
if ENVIRONMENT in ['local', 'dev', 'development']:
    SESSION_COOKIE_NAME = 'sessionid_dev'
    CSRF_COOKIE_NAME = 'csrftoken_dev'

    # Disable CSRF middleware locally to avoid 400s caused by corrupt cookies during debug
    MIDDLEWARE = [mw for mw in MIDDLEWARE if mw != 'django.middleware.csrf.CsrfViewMiddleware']

    # Verbose logging to identify exact Bad Request reasons during development
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
