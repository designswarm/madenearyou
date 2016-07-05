from django.contrib.gis.db import models


class VisibleProducersManager(models.GeoManager):
    """Returns visible Producers."""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)

