# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-28 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import program.models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0045_event_proposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventproposal',
            name='slides',
            field=models.FileField(blank=True, help_text='Upload your slides (PDF files only)', upload_to=program.models.slide_path, validators=[program.models.pdf_only]),
        ),
    ]