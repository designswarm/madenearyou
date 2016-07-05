from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Producer


class HomeView(TemplateView):
    template_name = 'producers/home.html'

class ProducerDetailView(DetailView):
    model = Producer

