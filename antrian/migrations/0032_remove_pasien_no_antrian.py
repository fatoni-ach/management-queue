# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 18:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0031_pasien_no_antrian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pasien',
            name='no_antrian',
        ),
    ]