# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-04-01 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0009_auto_20200402_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='durasi_pengobatan',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
