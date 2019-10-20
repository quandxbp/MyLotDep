"""
Django settings for ldserver project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from common.credentials import DATABASE_CRE

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+16m6_*vx4g71&y^bs&$-5r!eqefzo@s5du1)^*^trc#v^d7!b'
CSRF_COOKIE_SECURE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom App
    'product.apps.ProductConfig',
    'product_tiki.apps.ProductTikiConfig',
    'product_adayroi.apps.ProductAdayroiConfig',
    'timeseries.apps.TimeseriesConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ldserver.urls'

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

WSGI_APPLICATION = 'ldserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# DATABASE_ROUTERS = ['manager.router.DatabaseAppsRouter']

DATABASES = {
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'lotdep-timeseries',
    #     'AUTH_SOURCE': 'lotdep-timeseries',
    #     'HOST': 'mongodb://quandxbp:Hungvuong12@ds333248.mlab.com:33248/lotdep-timeseries',
    #     'USER': 'quandxbp',
    #     'PASSWORD': 'Hungvuong12',
    #     'PORT': 33248
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_CRE['DB_NAME'],
        'USER': DATABASE_CRE['USER'],
        'PASSWORD': DATABASE_CRE['PASSWORD'],
        'HOST': DATABASE_CRE['HOST'],
        'PORT': DATABASE_CRE['PORT'],
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'