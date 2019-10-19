# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 19:04
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0003_rowview_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rowview',
            name='filter',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Preselect rows satisfying this condition', null=True),
        ),
    ]