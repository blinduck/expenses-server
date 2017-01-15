# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 04:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='record',
            name='household',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Household'),
        ),
        migrations.AddField(
            model_name='user',
            name='household',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Household'),
        ),
    ]