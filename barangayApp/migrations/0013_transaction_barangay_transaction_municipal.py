# Generated by Django 4.2.1 on 2023-11-14 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0012_alter_economic_basis_of_payment_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='barangay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='barangayApp.barangay'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='municipal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='barangayApp.municipal'),
        ),
    ]
