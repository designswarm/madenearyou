from django.contrib import admin
from django.contrib.gis.db import models
from django.forms import CheckboxSelectMultiple

from .models import Product, Producer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'time_created',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'order', )
        }),
        ('Meta', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'time_created',)

    fieldsets = (
        (None, {
            'fields': ('business_name', 'contact_name', 'phone', 'email',
                        'url', 'products', )
        }),
        ('Location', {
            'fields': ('postcode', 'point',)
        }),
        ('Meta', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

