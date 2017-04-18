# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtgdb', '0007_auto_20170129_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('hash', models.CharField(db_index=True, max_length=40, verbose_name='hash')),
                ('text', models.TextField(verbose_name='text')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='rulings',
            field=models.ManyToManyField(to='mtgdb.Ruling'),
        ),
    ]
