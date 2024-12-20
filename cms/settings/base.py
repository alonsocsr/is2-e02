from pathlib import Path
from decouple import config

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    'home',
    'permissions',
    'categories',
    'profiles',
    'content',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'ckeditor_uploader',
    'sorl.thumbnail',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # requeridos para subir media files a cloudinary
    'cloudinary_storage',
    'cloudinary',
]

DISQUS_WEBSITE_SHORTNAME = 'cmsis2'
SESSION_COOKIE_SECURE = True


CSRF_COOKIE_SECURE = True  


SESSION_COOKIE_SAMESITE = 'None'  
CSRF_COOKIE_SAMESITE = 'None'  

# configuracion de ckeditor
CKEDITOR_UPLOAD_PATH = 'content/ckeditor'
CKEDITOR_ALLOW_NONIMAGE_FILES=True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 450,
        'width': 800,
        'removePlugins': 'exportpdf',
        'extraPlugins': ','.join([
          'youtube',
          'uploadimage',  
          'embed', 'autoembed', 'embedsemantic', 
        ])
    }
}
config.filebrowserBrowseUrl = '/browser/browse.php';
config.filebrowserUploadUrl = '/uploader/upload.php';


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, "templates/home"),
            BASE_DIR / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'home.context_processors.categorias_context',
                'home.context_processors.is_only_suscriptor',
            ],
        },
    },
]

WSGI_APPLICATION = 'cms.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_TZ = True
# settings.py

LANGUAGE_CODE = 'es'

USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = "/files/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

SITE_ID = 1
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = False        # True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'         # mandatory
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SINGUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_UNIQUE_EMAIL = True
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


ACCOUNT_RATE_LIMITS = {
    "login.failed": "3/1m",
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_SUBJECT_PREFIX = "Stark CMS - "
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Reemplaza con tu dirección de Gmail
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# Reemplaza con tu contraseña de Gmail
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# Reemplaza con tu dirección de Gmail
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
# ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Stark '
# CSRF_TRUSTED_ORIGINS = ['http://localhost:1337']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : config('CLOUD_NAME'),
    'API_KEY' : config('CLOUD_API_KEY'),
    'API_SECRET' : config('CLOUD_API_SECRET')
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-sorl-thumbnail-cache",
    }
}

THUMBNAIL_CACHE = 'default'
THUMBNAIL_CACHE_TIMEOUT = 3600


THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage'