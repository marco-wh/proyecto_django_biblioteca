# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2025-01-24 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0006_auto_20250124_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='libro',
            name='fecha_publicacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
