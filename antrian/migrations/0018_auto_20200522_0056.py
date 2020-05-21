# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0017_pasien_no_antrian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pasien',
            name='no_antrian',
        ),
        migrations.AddField(
            model_name='noantrian',
            name='pasien',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='antrian.Pasien'),
        ),
    ]