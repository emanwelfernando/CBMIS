# Generated by Django 4.2.1 on 2023-10-18 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0004_remove_barangay_municipal_barangay_geom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay',
            name='id_3',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='barangay',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='barangay',
            name='name_2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='municipal',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
