# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-14 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_caja_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='iva',
            field=models.BooleanField(default=False, verbose_name='aplica IVA'),
        ),
    ]
