# coding=utf-8
"""
Django settings for noVNC-Proxy-Django project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$8n81tj^32!$=tozs2lbg0mre=q(wxmy=tx-!4rxa@m)%dansu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '192.168.1.112', '85.240.2.211']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'revproxy',
#    'django_otp',
#    'django_otp.plugins.otp_totp',
    # Application
    'app',
    'rest_framework',
    'apikeys',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['',
            os.path.join(BASE_DIR, 'templates'),
            'django.template.loaders.filesystem.Loader',
        ],
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-PT'

# TIME_ZONE = 'Greenwitch'
TIME_ZONE = 'Europe/Lisbon'


# Set the variable TIME_ZONE to Greenwitch time zone


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

#STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / 'novnc-proxy-django-master/static']


STATIC_URL = 'static/'
STATICFILES_DIRS = [(os.path.join(BASE_DIR, 'static'))]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#if DEBUG:
#    STATICFILES_DIRS = ('', os.path.join(BASE_DIR, 'static'))
#else:
#    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'


VNC_PROXY_HOST = '127.0.0.1'
VNC_PROXY_PORT = '5900'

# Session timeout control
#SESSION_COOKIE_AGE = 60
#SESSION_EXPIRE_AT_BROWSER_CLOSE=True # Invalid session
#SESSION_EXPIRE_SECONDS = 600 # 5 minutes
#SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_TIMEOUT_REDIRECT = '/'

