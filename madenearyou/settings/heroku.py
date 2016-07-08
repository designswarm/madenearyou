from .defaults import *

import dj_database_url
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

ALLOWED_HOSTS = [".herokuapp.com",]

# Set up for django-storages to store Media files on S3.

INSTALLED_APPS += ['storages', ]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.setdefault('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.setdefault('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.setdefault('AWS_STORAGE_BUCKET_NAME', '')

