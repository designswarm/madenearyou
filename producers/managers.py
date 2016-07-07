from django.contrib.gis.db import models


class VisibleProducerImagesManager(models.Manager):
    """Returns visible Producers Images."""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class VisibleProducersManager(models.GeoManager):
    """Returns visible Producers."""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)

