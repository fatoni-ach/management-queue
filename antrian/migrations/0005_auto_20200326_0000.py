# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-03-25 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0004_auto_20200325_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
