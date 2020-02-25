import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .defaults import *


DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

ALLOWED_HOSTS = [".herokuapp.com", "www.madenearyou.org", "madenearyou.org",]

# Set up for django-storages to store Media files on S3.

INSTALLED_APPS += ['storages', ]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.setdefault('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.setdefault('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.setdefault('AWS_STORAGE_BUCKET_NAME', '')


sentry_sdk.init(
    dsn="https://367a1b2fecd9410889dc51e100e51bf9@sentry.io/2864349",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
