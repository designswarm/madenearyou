# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0003_auto_20160705_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.PositiveSmallIntegerField(default=10, help_text='Products are ordered by this number.'),
        ),
    ]
