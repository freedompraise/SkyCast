
from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import mimetypes
# Build paths inside the project like this: BASE_DIR / 'subdir'.
mimetypes.add_type("text/css", ".css", True)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(' ')

APPEND_SLASH=False

SECRET_KEY = os.getenv('SECRET_KEY')

load_dotenv(BASE_DIR / '.env')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'src',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'weatherApp.urls'

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


WSGI_APPLICATION = 'weatherApp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}


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

SESSION_COOKIE_AGE = 1800 # user session time of 30 mins


MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = config('MAILCHIMP_DATA_CENTER')
MAILCHIMP_EMAIL_LIST_ID = config('MAILCHIMP_EMAIL_LIST_ID')
OPEN_WEATHER_API_KEY = config('OPEN_WEATHER_API_KEY')

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# define the location of your static files
STATIC_URL = '/static/'

MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'images')

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_HSTS_SECONDS = 315300 # or any value that you prefer

# set SECURE_SSL_REDIRECT to True to enforce SSL connection
SECURE_SSL_REDIRECT = True

# set SECURE_HSTS_INCLUDE_SUBDOMAINS to True if all subdomains should be served via SSL
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# set SECURE_HSTS_PRELOAD to True to submit your site to the browser preload list
SECURE_HSTS_PRELOAD = True

# set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE to True to use secure-only cookies
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True