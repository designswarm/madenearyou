from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.gis import geos, measure
from django.contrib.gis.db.models.functions import Distance
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import ProducerForm, ProducerAdminForm, FindProducerForm, ProducerImageFormset
from .models import Producer

from . import validators
from .postcoder import Postcoder, PostcoderException


class FlatPageMixin(object):
    """
    Retrieves the FlatPage object for the specified url, and includes it in the
    context.

    If no url is specified, request.path is used.

    From https://blog.schwuk.com/2013/02/26/flatpages-content-in-other-views/
    """
    url = None

    def get_context_data(self, **kwargs):
        if not self.url:
            self.url = self.request.path

        context = super().get_context_data(**kwargs)
        try:
            flatpage = FlatPage.objects.get(url=self.url)
            flatpage.title = mark_safe(flatpage.title)
            flatpage.content = mark_safe(flatpage.content)
            context["flatpage"] = flatpage
        except FlatPage.DoesNotExist:
            context["flatpage"] = None

        return context


class HomeView(FlatPageMixin, ListView):
    "Uses content from a Flatpage."

    template_name = 'producers/home.html'
    model = Producer
    queryset = Producer.visible_objects.all()
    paginate_by = 20


@method_decorator([csrf_protect, never_cache], name='dispatch')
class ProducerAddView(FormView):
    template_name = 'producers/producer_add.html'
    success_url = reverse_lazy('producer_add_thanks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'image_formset' not in context:
            context['image_formset'] = ProducerImageFormset()

        # If there was an error, the image upload fields don't have their
        # previous values attached. So the best we can do is to notice when
        # images were submitted, and mention this in the template.
        context['num_images_submitted'] = len(self.request.FILES)

        return context

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        if self.request.user.is_superuser:
            return ProducerAdminForm
        else:
            return ProducerForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_formset = ProducerImageFormset(request.POST, request.FILES)

        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form, image_formset)

    def form_valid(self, form, image_formset):
        "Both form and formset are valid, so save them."
        producer = form.save()
        image_formset.instance = producer
        img = image_formset.save()

        if producer.is_visible:
            # Presumably added by an admin, so we can see it:
            return HttpResponseRedirect(reverse_lazy('producer_detail',
                                                    kwargs={'pk': producer.pk}))
        else:
            # Added by a normal user, so not visible yet:
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_formset):
        return self.render_to_response(self.get_context_data(
                                    form=form, image_formset=image_formset))


@method_decorator([csrf_protect, never_cache], name='dispatch')
class MapView(FormView):
    template_name = 'producers/find.html'
    form_class = FindProducerForm

    # We'll look for Producers within this many kilometres:
    max_km = 40

    def get_initial(self):
        "If we have pc=blah in the URL, use that as the default in the form."
        initial = super().get_initial()
        pc = self.request.GET.get('pc', None)
        if pc:
            initial['postcode'] = pc
        return initial

    def get_success_url(self):
        pc = self.request.POST.get('postcode', None)
        if pc:
            getstr = urlencode({'pc': pc})
            return '%s?%s' % (reverse_lazy('producers_map'), getstr)
        else:
            return reverse_lazy('producers_map')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Includes the map JS:
        context['include_map'] = True
        context['max_km'] = self.max_km

        pc = self.request.GET.get('pc')
        if pc:
            pc = pc.upper().strip()
            try:
                validators.validate_uk_postcode(pc)
                context['postcode'] = pc
                producers_context = self.get_producers_context(pc)
                # Combine the two dicts, python 3.5 way:
                context = {**context, **producers_context}
            except:
                # Postcode didn't validate.
                pass
        return context

    def get_producers_context(self, postcode):
        """
        Tries to geocode the postcode, then fetch Producers near to that.

        Returns a dict containing:
            producers: Empty list or a queryset.
            geolocation_error: String, if something went wrong.

        Additionally, if we geocoded successfully:
            latitude: Of the postcode
            longitude: Of the postcode
        """

        context = {
            'producers': [],
        }

        try:
            latlon = Postcoder().geolocate(postcode)
        except PostcoderException as e:
            context['geolocation_error'] = "We couldn't find the location of the postcode '%s'." % postcode
            return context

        # Make a point where this postcode is:
        point = 'POINT(%s %s)' % (latlon['longitude'], latlon['latitude'])
        center = geos.fromstr(point)

        # How far away do we fetch?
        dist = {'km': self.max_km}

        # Get the producers within dist:
        producers = Producer.objects.filter(
                            point__distance_lte=(center, measure.D(**dist)))

        # Add a 'distance' property to them, showing distance from center:
        producers = producers.annotate(distance=Distance('point', center))
        producers = producers.order_by('distance')

        context['latitude'] = latlon['latitude']
        context['longitude'] = latlon['longitude']
        context['producers'] = producers

        return context


class ProducerDetailView(DetailView):
    model = Producer
    queryset = Producer.visible_objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Includes the map JS:
        context['include_map'] = True
        return context
