# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-04-01 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0008_datapasien_noantrian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='durasi_pengobatan',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
