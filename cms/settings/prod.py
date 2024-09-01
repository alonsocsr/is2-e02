from .base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'vercel.app', '.now.sh']

STATICFILES_STORAGES = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('PGDATABASE'),
    'USER': os.getenv('PGUSER'),
    'PASSWORD': os.getenv('PGPASSWORD'),
    'HOST': os.getenv('PGHOST'),
    'PORT': os.getenv('PGPORT', 5432),
    'OPTIONS': {
      'sslmode': 'require',
    },
  }
}