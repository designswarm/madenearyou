from .defaults import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'madenearyou',
        'USER': 'madenearyou',
        'PASSWORD': 'madenearyou',
        'HOST': 'localhost',
        'PORT': '',
    }
}
