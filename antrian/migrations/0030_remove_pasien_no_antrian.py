# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 18:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0029_auto_20200522_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pasien',
            name='no_antrian',
        ),
    ]
