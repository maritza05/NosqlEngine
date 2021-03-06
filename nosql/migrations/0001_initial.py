# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
            options={
                'verbose_name': 'datamodel',
                'ordering': ('name',),
                'verbose_name_plural': 'datamodels',
            },
        ),
        migrations.CreateModel(
            name='Nosql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60)),
                ('slug', models.SlugField(max_length=60)),
                ('official_website', models.URLField()),
                ('datamodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nosqls', to='nosql.DataModel')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterIndexTogether(
            name='nosql',
            index_together=set([('id', 'slug')]),
        ),
    ]
