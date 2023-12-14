# Generated by Django 4.2.1 on 2023-10-18 17:55

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0003_customuser_barangay_customuser_municipal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barangay',
            name='municipal',
        ),
        migrations.AddField(
            model_name='barangay',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='municipal',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
    ]
