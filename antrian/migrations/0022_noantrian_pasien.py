# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0021_remove_noantrian_pasien'),
    ]

    operations = [
        migrations.AddField(
            model_name='noantrian',
            name='pasien',
            field=models.ForeignKey(default=40, on_delete=django.db.models.deletion.CASCADE, to='antrian.Pasien'),
        ),
    ]
