"""
Django settings for projeto project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os
import sys
from django.contrib.messages import constants
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# gerando a secret_key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# configurando os host para serem pegos a partir das variáveis de ambiente
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","127.0.0.1,localhost").split(",")

SECURE_SSL_REDIRECT = False
if os.getenv("DJANGO_SECURE_SSL_REDIRECT", "True") == "True":
    SECURE_SSL_REDIRECT = True

# configurando o DEBUG a partir de uma variável de ambiente
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Essa variável de ambiente irá definir se queremos usar o sqlite ou a database postgree
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Application definition
LOGIN_URL = '/admin'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    "configs",
    'django.contrib.humanize'
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

ROOT_URLCONF = 'projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'projeto.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
        }
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
MEDIA_URL = "media/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static')
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    constants.ERROR: "alert-danger",
    constants.WARNING: "alert-warning",
    constants.SUCCESS: "alert-success",
    constants.INFO: 'alert-info'
}

#definindo cookie 
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 # 7 dias