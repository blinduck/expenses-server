# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-22 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170115_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
