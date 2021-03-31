from .defaults import *
from glob import glob


DEBUG = True

# For GeoDjango https://stackoverflow.com/a/62966945/250962
GDAL_LIBRARY_PATH = glob("/usr/lib/libgdal.so.*")[0]
GEOS_LIBRARY_PATH = glob("/usr/lib/libgeos_c.so.*")[0]


# Debug Toolbar settings.
if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    INTERNAL_IPS = ["127.0.0.1"]

    RESULTS_CACHE_SIZE = 100

    # Stop Django handling static files in favour of Whitenoise.
    # (When DEBUG = False)
    # Need to add the app just before staticfiles, so:
    new_apps = []
    for app in INSTALLED_APPS:
        if app == "django.contrib.staticfiles":
            new_apps.append("whitenoise.runserver_nostatic")
        new_apps.append(app)
    INSTALLED_APPS[:] = new_apps
