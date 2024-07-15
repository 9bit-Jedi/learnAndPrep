"""
Django settings for learnAndPrep project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
from datetime import timedelta



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '52.72.21.105', 'stage.vjnucleus.com'] 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'auth_service.apps.AuthServiceConfig',
    'questions.apps.QuestionsConfig',
    'uploader.apps.UploaderConfig',
    'quiz.apps.QuizConfig',
    # 'mockTest.apps.MocktestConfig',
    'notes.apps.NotesConfig',
    # 'mentorship.apps.MentorshipConfig',
    'contactUs.apps.ContactusConfig',
    'rest_framework',
    # "debug_toolbar",
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    'accounts',
    'mentorship',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'learnAndPrep.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'learnAndPrep.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('PGHOST'),
        'NAME': config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'PORT': config('PGPORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
  }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, 
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=40),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM':'jti',
    }

AUTH_USER_MODEL = 'accounts.User'

PASSWORD_RESET_TIMEOUT = 900

# [STAGE/PROD] AWS Configuration

# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

# AWS_S3_REGION_NAME = 'us-east-1' 

# # AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_FILE_OVERWRITE = False 

# AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/' 
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# [DEV] static files & media in root dir

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# OTP Email Configuration
OTP_EMAIL_HOST_USER = config('OTP_EMAIL_USER')
OTP_EMAIL_HOST_PASSWORD = config('OTP_EMAIL_PASSWORD')

# Support Email Configuration
SUPPORT_EMAIL_HOST_USER = config('SUPPORT_EMAIL_USER')
SUPPORT_EMAIL_HOST_PASSWORD = config('SUPPORT_EMAIL_PASSWORD')

DEFAULT_FROM_EMAIL = SUPPORT_EMAIL_HOST_USER

#######

PHONE_NUMBER_ID = config('PHONE_NUMBER_ID')
WHATSAPP_AUTH_TOKEN = config('WHATSAPP_AUTH_TOKEN')

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://52.72.21.105',
    'http://stage.vjnucleus.com',
    'http://www.stage.vjnucleus.com',
    'http://vjn-staging-bucket.s3-website-us-east-1.amazonaws.com'
]
# CORS_ALLOW_ALL_ORIGINS = True

TIME_ZONE = 'Asia/Kolkata'

# HTTPS SETTINGS
SESSION_COOKIE_SECURE = False               # Set to True if you are using HTTPS (recommended)
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False                 # Set to True if you are using HTTPS (recommended)

# HSTS SETTINGS
# SECURE_HSTS_SECONDS = 31536000              # Set to 0 if you are not using HTTPS
# SECURE_HSTS_PRELOAD = True 
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SESSION_COOKIE_SAMESITE = 'Lax'             # Adjust if needed, depending on your specific requirements
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False                # Set to False to allow frontend access to the CSRF token