# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0030_remove_pasien_no_antrian'),
    ]

    operations = [
        migrations.AddField(
            model_name='pasien',
            name='no_antrian',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='antrian.NoAntrian'),
        ),
    ]
