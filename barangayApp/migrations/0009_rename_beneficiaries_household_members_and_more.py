# Generated by Django 4.2.1 on 2023-10-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0008_household_num_members_per_households_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='beneficiaries',
            new_name='members',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='num_members_per_households',
            new_name='num_members',
        ),
        migrations.AddField(
            model_name='household',
            name='access_to_basic_amenities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='education_level_of_head',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='household_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='housing_condition',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='languages_spoken',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='monthly_income_range',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='occupation_of_members',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='ownership_of_assets',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='special_needs',
            field=models.TextField(blank=True, null=True),
        ),
    ]