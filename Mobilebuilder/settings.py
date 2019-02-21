"""
Django settings for Mobilebuilder project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's()@4rom4@ni45odmls(y9*@9iq21uz*bg4=b+rez!1x@x&x26'

# SECURITY WARNING: don't run with debug turned on in produ88000000ction!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'authentication',
    'schema',
    'home',
    'project',
    'transaction',
    'transactionview',
    'usersetup',
    'reportview',
    'logintemplate',
    'hometemplate',
    'actions',
    'generateprocess',
    'schemageneration',
    'syncmaster',
    'rest_framework',
    'corsheaders',
    'sslserver',
    'aldjemy',
    'master',    
    'rolesetup',
    'smssetup',
    'notification',
    'printformat',
    'eventconfiguration'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'Mobilebuilder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'Mobilebuilder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aishwarya',
        'USER':'root',
        'PASSWORD':'12345',
        'HOST':'192.168.125.173',
        'PORT':'3306',
   
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = "C:\Users\PRIYA\Desktop\Mobilebuilder\static"

STATICFILES_DIRS = (
     os.path.join(BASE_DIR, "static"),
)

# url to redirect after successfull login
LOGIN_REDIRECT_URL = "/home/main/"


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MEDIA_ROOT = "E:/Mobilebuilder/"


# Logging settings for django projects, works with django 1.5+
# If DEBUG=True, all logs (including django logs) will be
# written to console and to debug_file.
# If DEBUG=False, logs with level INFO or higher will be
# saved to production_file.
# Logging usage:

# import logging
# logger = logging.getLogger(__name__)
# logger.info("Log this message")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue'
#         }
#     },
#     'formatters': {
#         'main_formatter': {
#             'format': '%(levelname)s:%(name)s: %(message)s '
#                       '(%(asctime)s; %(filename)s:%(lineno)d)',
#             'datefmt': "%Y-%m-%d %H:%M:%S",
#         },
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'main_formatter',
#         },
#         'production_file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/main.log',
#             'maxBytes': 1024 * 1024 * 5,  # 5 MB
#             'backupCount': 7,
#             'formatter': 'main_formatter',
#             'filters': ['require_debug_false'],
#         },
#         'debug_file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/main_debug.log',
#             'maxBytes': 1024 * 1024 * 5,  # 5 MB
#             'backupCount': 7,
#             'formatter': 'main_formatter',
#             'filters': ['require_debug_true'],
#         },
#         'null': {
#             "class": 'logging.NullHandler',
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins', 'console'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['null', ],
#         },
#         'py.warnings': {
#             'handlers': ['null', ],
#         },
#         '': {
#             'handlers': ['console', 'production_file', 'debug_file'],
#             'level': "DEBUG",
#         },
#     }
# }