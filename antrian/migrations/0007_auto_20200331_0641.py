# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-03-30 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0006_auto_20200326_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='durasi_pengobatan',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pasien',
            name='jenis_kelamin',
            field=models.CharField(choices=[('l', 'L'), ('p', 'P')], default='l', max_length=10),
        ),
        migrations.AlterField(
            model_name='pasien',
            name='umur',
            field=models.IntegerField(blank=True),
        ),
    ]
