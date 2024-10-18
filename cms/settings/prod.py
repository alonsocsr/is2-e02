from .base import *

from django.core.files.storage import FileSystemStorage

SECRET_KEY = config('SECRET_KEY')

DEBUG = False
DISQUS_DEVELOPER = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.now.sh']

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB_PROD'),
        'USER': config('POSTGRES_USER_PROD'),
        'PASSWORD': config('POSTGRES_PASSWORD_PROD'),
        'HOST': config('POSTGRES_HOST_PROD'),
        'PORT': config('POSTGRES_PORT_PROD'),
    }
}


CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : config('CLOUD_NAME'),
    'API_KEY' : config('CLOUD_API_KEY'),
    'API_SECRET' : config('CLOUD_API_SECRET')
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-sorl-thumbnail-cache",
    }
}

THUMBNAIL_CACHE = 'default'
THUMBNAIL_CACHE_TIMEOUT = 3600


THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage'