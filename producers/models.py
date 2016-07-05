import logging

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from . import managers
from .postcoder import Postcoder, PostcoderException
from .validators import validate_uk_phone_number, validate_uk_postcode


logger = logging.getLogger(__name__)


class TimeStampedModelMixin(models.Model):
    "Should be mixed in to all models."

    time_created = models.DateTimeField(auto_now_add=True,
                help_text="The time this item was created in the database.")
    time_modified = models.DateTimeField(auto_now=True,
                help_text="The time this item was last saved to the database.")

    class Meta:
        abstract = True


class Product(TimeStampedModelMixin, models.Model):
    name = models.CharField(blank=False, null=False, max_length=30)
    slug = models.SlugField(blank=False, null=False, max_length=30,
            unique=True, help_text="Used in URLs referring to this product.")
    order = models.PositiveSmallIntegerField(blank=False, null=False,
            default=10,
            help_text="Products are ordered by this number.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Producer(TimeStampedModelMixin, models.Model):

    business_name = models.CharField(blank=False, null=False, max_length=255)
    contact_name = models.CharField(blank=True, null=False, max_length=255)
    postcode = models.CharField(blank=False, null=False,
                            validators=[validate_uk_postcode], max_length=8)
    phone = models.CharField(blank=False, null=False,
                        validators=[validate_uk_phone_number], max_length=15)
    email = models.EmailField(blank=False, null=False)
    url = models.URLField(blank=True, null=False, verbose_name="URL")

    point = models.PointField(srid=4326, blank=True, null=True)

    is_visible = models.BooleanField(default=False,
            help_text="Check box to make this Producer visible on the site.")

    products = models.ManyToManyField(Product)

    objects = models.GeoManager()
    # Only producers with is_visible=True:
    visible_objects = managers.VisibleProducersManager()

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        #self.point = Point(self.longitude, self.latitude)
        self.postcode = self.postcode.strip().upper()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['business_name']


@receiver(pre_save, sender=Producer)
def set_location(sender, instance, **kwargs):
    """
    Tries to set the lat/lon of the Producer when it's saved, based on the
    postcode.

    If the postcode has changed, or Producer is brand new, we look up lat/lon.

    If found, we set the Producer.point value.

    If we can't find lat/lon we set Producer.point to None.
    """

    set_point = False

    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new.
        set_point = True
    else:
        if not obj.postcode == instance.postcode:
            # Postcode has changed.
            set_point = True

    if set_point:
        try:
            latlon = Postcoder().geolocate(instance.postcode)
            point = "POINT(%s %s)" % (latlon['longitude'], latlon['latitude'])
            instance.point = geos.fromstr(point)
        except PostcoderException as e:
            logger.error('Error trying to geolocate "%s": %s' % \
                                                (instance.postcode, str(e)))
            # Unset whatever's there.
            instance.point = None

