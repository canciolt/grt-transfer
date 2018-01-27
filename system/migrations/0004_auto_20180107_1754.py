# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-07 17:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_combustible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pista',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('litros', models.FloatField(verbose_name='litros')),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='combustible',
            name='camion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comb_camion', to='system.Camion', verbose_name='camion'),
        ),
        migrations.AlterField(
            model_name='combustible',
            name='operador_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comb_operador', to='system.Operador', verbose_name='operador'),
        ),
    ]