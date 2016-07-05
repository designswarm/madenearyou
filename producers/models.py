from django.contrib.gis.db import models

from .validators import validate_uk_phone_number, validate_uk_postcode


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
    email = models.EmailField(blank=True, null=False)
    url = models.URLField(blank=True, null=False, verbose_name="URL")

    #latitude = models.FloatField(null=True, blank=True)
    #longitude = models.FloatField(null=True, blank=True)
    point = models.PointField(srid=4326, blank=True)

    products = models.ManyToManyField(Product)

    objects = models.GeoManager()

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        #self.point = Point(self.longitude, self.latitude)
        self.postcode = self.postcode.upper()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['business_name']



