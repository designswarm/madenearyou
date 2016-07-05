from .defaults import *

DEBUG = False

ALLOWED_HOSTS = ["*",]

# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'madenearyou',
        'USER': 'madenearyou',
        'PASSWORD': 'madenearyou',
        'HOST': 'localhost',
        'PORT': '',
    }
}

