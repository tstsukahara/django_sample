# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-19 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talkapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]
