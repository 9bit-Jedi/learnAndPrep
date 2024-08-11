
from .settings_base import *


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '299f-103-37-201-176.ngrok-free.app'] 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': config('PGHOST'),
    #     'NAME': config('PGDATABASE'),
    #     'USER': config('PGUSER'),
    #     'PASSWORD': config('PGPASSWORD'),
    #     'PORT': config('PGPORT'),
    #     'OPTIONS': {
    #         'sslmode': 'require',
    #     },
}

# [DEV] static files & media in root dir

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://13.202.87.212',
]

print("using dev settings")
