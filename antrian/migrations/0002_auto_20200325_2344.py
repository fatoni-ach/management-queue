# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-03-25 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Antrian',
            new_name='Pasien',
        ),
    ]
