from django.db.models import Manager


class VisibleProducerImagesManager(Manager):
    """Returns visible Producers Images."""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class VisibleProducersManager(Manager):
    """Returns visible Producers."""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)
