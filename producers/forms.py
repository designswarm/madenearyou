from django import forms
from .models import Producer, Product
from django.contrib.gis.geos import Point

from . import validators


attrs = {'class': 'form-control'}
required_attrs = {'class': 'required form-control'}


class ProducerForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    honeypot = forms.CharField(required=False,
                            label='If you enter anything in this field '\
                                'your registration will be treated as spam')

    class Meta:
        model = Producer
        fields = ['business_name', 'contact_name', 'postcode', 'phone',
                    'email', 'url', 'products', ]

        # Adding attributes to the form fields.
        widgets = {
            'business_name':    forms.TextInput(attrs=required_attrs),
            'contact_name':     forms.TextInput(attrs=attrs),
            'postcode':         forms.TextInput(attrs=required_attrs),
            'phone':            forms.TextInput(attrs=required_attrs),
            'email':            forms.EmailInput(attrs=required_attrs),
            'url':              forms.URLInput(attrs=required_attrs),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For some reason need to do this to use checkboxes for Products:
        # via http://www.joshuakehn.com/2013/6/23/django-m2m-modelform.html
        self.fields['products'].help_text = ''
        self.fields['products'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['products'].queryset = Product.objects.all()

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

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


