from django.conf.urls import url
from django.contrib.flatpages import views as flatpages_views
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$',
        views.HomeView.as_view(),
        name='home'),

    # We add Flatpages here, rather than use the middleware, so that we can
    # easily link to a Flatpage by name in the templates.
    url(r'^about/$',
        flatpages_views.flatpage, {'url': '/about/'}, name='about'),

    # So we can test these templates when DEBUG=True.
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),

    url(r'^map/$',
        views.MapView.as_view(),
        name='producers_map'),

    url(r'^producer/add/$',
        views.ProducerAddView.as_view(),
        name='producer_add'),

    url(r'^producer/add/thanks/$',
        views.ProducerAddThanksView.as_view(),
        name='producer_add_thanks'),

    url(r'^producer/(?P<pk>\d*)/$',
        views.ProducerDetailView.as_view(),
        name='producer_detail'),
]
