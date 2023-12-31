# Generated by Django 4.2.1 on 2023-11-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0020_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
