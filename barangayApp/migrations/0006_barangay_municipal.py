# Generated by Django 4.2.1 on 2023-10-18 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0005_alter_barangay_id_3_alter_barangay_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay',
            name='municipal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangayApp.municipal'),
        ),
    ]
