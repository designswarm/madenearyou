from .defaults import *

DEBUG = True

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

# Debug Toolbar settings.
if DEBUG:
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INSTALLED_APPS += ['debug_toolbar', ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        # Force the toolbar to show as INTERNAL_IPS wasn't working with Vagrant.
        'SHOW_TOOLBAR_CALLBACK': "%s.true" % __name__
    }
    INTERNAL_IPS = ['127.0.0.1', '192.168.33.1', '0.0.0.0']
    RESULTS_CACHE_SIZE = 100

    def true(request):
        return True

