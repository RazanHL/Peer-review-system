"""
Django settings for Journal project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool) 

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app", ".now.sh"] #, "*Journal.vercel.app" ,"*"] 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    'django_filters',
    # third party:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.linkedin',
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'rosetta',
    'notifications',
    # local:
    'profiles',
    'pages',
    'articles',
    'mlapplications',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'Journal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Journal/templates'],
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

WSGI_APPLICATION = 'Journal.wsgi.application'

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     # 'ENGINE': 'django.db.backends.sqlite3',
    #     # 'NAME': BASE_DIR / 'db.sqlite3',
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': config('DATABASE_NAME'),
    #     'USER': config('DATABASE_USER'), 
    #     'PASSWORD': config('DATABASE_PASSWORD'),
    #     'HOST': config('DATABASE_HOST'),
    #     'PORT': config('DATABASE_PORT'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#_psycopg2',
        'NAME': config('REMOTEDATABASE_NAME'),
        'USER': config('REMOTEDATABASE_USER'), 
        'PASSWORD': config('REMOTEDATABASE_PASSWORD'),
        'HOST': config('REMOTEDATABASE_HOST'),
        'PORT': config('REMOTEDATABASE_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

TIME_ZONE = 'Asia/Damascus' #'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [BASE_DIR / 'Journal/static', ]
STATICFILES_DIRS = [os.path.join(BASE_DIR, '/Journal/static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build' ,'Journal/static')


MEDIA_URL = 'media/'
MEDIA_ROOT = (BASE_DIR / 'Journal/media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'account_login' # requests are redirected for login when we are trying to limit access to certain pages
LOGIN_REDIRECT_URL =   '/profiles/wherenext/' #  "users-profile"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT = "home"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    # 'social_core.backends.linkedin.LinkedinOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',    
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
    },
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress',
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]  
    }
}
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

