# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nosql', '0004_auto_20161119_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='nosql',
            name='official_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='nosql',
            name='stack_description',
            field=models.TextField(blank=True),
        ),
    ]
