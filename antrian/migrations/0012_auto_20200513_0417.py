# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-05-12 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0011_auto_20200512_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='noantrian',
            name='durasi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='noantrian',
            name='no',
            field=models.IntegerField(default=0),
        ),
    ]