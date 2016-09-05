from django import forms
from django.conf import settings
from django.contrib.gis.geos import Point
from django.forms import inlineformset_factory

from captcha.fields import ReCaptchaField

from . import validators
from .models import Producer, ProducerImage, Product


attrs = {'class': 'form-control'}
required_attrs = {'class': 'form-control', 'required': 'required',}
postcode_attrs = {k:v for k,v in required_attrs.items()}
postcode_attrs['class'] = postcode_attrs['class'] + ' form-control-postcode'


class HoneypotFormMixin(forms.Form):
    "Provides a hidden field designed to prevent automated posting."
    honeypot = forms.CharField(required=False,
                            label='If you enter anything in this field '\
                                'your data will be treated as spam')

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value


class FindProducerForm(HoneypotFormMixin, forms.Form):
    postcode = forms.CharField(required=True, max_length=8,
                                widget=forms.TextInput(attrs=postcode_attrs))

    def clean_postcode(self):
        """Check postcode validity, as a format."""
        value = self.cleaned_data["postcode"]
        if value:
            validators.validate_uk_postcode(value)
        return value.strip()


class ProducerForm(HoneypotFormMixin, forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Producer
        # The order the fields will appear in the form:
        fields = ['business_name', 'postcode', 'contact_name',
                    'phone', 'email', 'url', 'products', ]

        # Adding attributes to the form fields.
        widgets = {
            'business_name':    forms.TextInput(attrs=required_attrs),
            'contact_name':     forms.TextInput(attrs=attrs),
            'postcode':         forms.TextInput(attrs=postcode_attrs),
            'phone':            forms.TextInput(attrs=required_attrs),
            'email':            forms.EmailInput(attrs=required_attrs),
            'url':              forms.URLInput(attrs=required_attrs),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For some reason need to do this to use checkboxes for Products:
        # via http://www.joshuakehn.com/2013/6/23/django-m2m-modelform.html
        self.fields['products'].help_text = 'This has to be food you make in the country and do not import'
        self.fields['products'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['products'].queryset = Product.objects.all()

        if settings.USE_RECAPTCHA:
            self.fields['captcha'] = ReCaptchaField(label="Anti-spam test")

    def clean_postcode(self):
        value = self.cleaned_data['postcode']
        if value:
            validators.validate_uk_postcode(value)
        return value.strip()

    def clean_phone(self):
        value = self.cleaned_data['phone']
        if value:
            validators.validate_uk_phone_number(value)
        return value.strip()


class ProducerAdminForm(ProducerForm):
    """
    A variation of the Producer form that only Admin users see, which has
    no captcha field and automatically sets the Producer to visible.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'captcha' in self.fields:
            del self.fields['captcha']

    def clean_products(self):
        v = self.cleaned_data['products']
        print(v)
        return v

    def save(self, commit=True):
        "Set `is_visible` to be true if added by an Admin."

        m = super().save(commit=False)
        m.is_visible = True

        if commit:
            m.save()
            self._save_m2m()

        return m


# For the part of the Producer form that lists 3 upload fields for images.
ProducerImageFormset = inlineformset_factory(Producer, ProducerImage,
                                                fields=('image',), max_num=3 )
