# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-24 13:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0002_storage_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Responsible person'),
        ),
    ]
