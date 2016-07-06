from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import ProducerForm
from .models import Producer


class HomeView(TemplateView):
    template_name = 'producers/home.html'


@method_decorator([csrf_protect, never_cache], name='dispatch')
class ProducerAddView(FormView):
    template_name = 'producers/producer_add.html'
    form_class = ProducerForm
    success_url = reverse_lazy('producer_add_thanks')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProducerAddThanksView(TemplateView):
    template_name = 'producers/producer_add_thanks.html'


class ProducerDetailView(DetailView):
    model = Producer
    queryset = Producer.visible_objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['include_map'] = True
        return context

