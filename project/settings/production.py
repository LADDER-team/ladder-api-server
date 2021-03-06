"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Import common settings
from project.settings.common import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['api.ladder.noframeschools.com', 'localhost']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'ladder'),
        'USER': os.environ['DB_USER'], # Raise error if not exists
        'PASSWORD': os.environ['DB_PASS'], # Raise error if not exists
        'HOST': os.environ['DB_HOST'], # Raise error if not exists
        'PORT': os.environ.get('DB_PORT', ''),
    }
}
