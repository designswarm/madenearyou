from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$',
        views.HomeView.as_view(),
        name='home'),

    # So we can test these templates when DEBUG=True.
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),

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
