# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-21 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0023_auto_20200522_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noantrian',
            name='pasien_fk',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='antrian.Pasien'),
        ),
    ]
