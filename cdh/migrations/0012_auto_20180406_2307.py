# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-06 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdh', '0011_auto_20171031_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mat_khau',
            field=models.CharField(max_length=200),
        ),
    ]
