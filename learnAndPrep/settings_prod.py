from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['13.202.87.212', 'vjnucleus.com'] 

DATABASES = {

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


# [STAGE/PROD] AWS Configuration

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'vjn-prod-s3'
AWS_S3_REGION_NAME = 'ap-south-1' 

# AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False 


AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/' 
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CORS_ALLOWED_ORIGINS = [
    'http://vjnucleus.com',
    'https://vjnucleus.com',
    'http://www.vjnucleus.com',
    'https://www.vjnucleus.com',
    'http://vjn-prod-s3.s3-website.ap-south-1.amazonaws.com',
    'https://vjn-prod-s3.s3-website.ap-south-1.amazonaws.com'
]

BASE_URL = 'https://vjnucleus.com'

print("using prod settings")