# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0008_auto_20160707_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producerimage',
            name='is_visible',
        ),
    ]
