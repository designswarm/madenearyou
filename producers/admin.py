from django.contrib import admin
from django.contrib.gis.db import models
from django.forms import CheckboxSelectMultiple

from imagekit.admin import AdminThumbnail

from .models import Producer, ProducerImage, Product


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


class ProducerImageInline(admin.TabularInline):
    model = ProducerImage
    extra = 3
    raw_id_fields = ('producer',)
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')

    fields = ('admin_thumbnail', 'image', )
    readonly_fields = ['admin_thumbnail']


def make_visible(modeladmin, request, queryset):
    queryset.update(is_visible=True)
make_visible.short_description = "Mark selected producers as visible"


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'is_visible', 'time_created',)
    actions = [make_visible]

    fieldsets = (
        (None, {
            'fields': ('business_name', 'is_visible', 'contact_name', 'phone', 'email',
                        'url', 'products', )
        }),
        ('Location', {
            'fields': ('postcode', 'point',)
        }),
        ('Meta', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('point', 'time_created', 'time_modified',)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    inlines = [
        ProducerImageInline,
    ]

