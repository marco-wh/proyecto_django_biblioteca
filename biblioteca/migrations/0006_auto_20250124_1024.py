# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2025-01-24 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0005_auto_20250124_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(upload_to='portadas'),
        ),
    ]
