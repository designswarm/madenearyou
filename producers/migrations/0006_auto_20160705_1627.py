# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 16:27
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0005_auto_20160705_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
