from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/$',
        views.HomeView.as_view(),
        name='home'),

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
