# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtgdb', '0009_auto_20170130_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='rulings',
            field=models.ManyToManyField(blank=True, to='mtgdb.Ruling'),
        ),
    ]
