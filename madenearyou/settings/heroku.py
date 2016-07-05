from .defaults import *

DEBUG = True


import dj_database_url
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

ALLOWED_HOSTS = [".herokuapp.com",]
