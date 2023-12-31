# Generated by Django 4.2.1 on 2023-11-19 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0014_remove_household_relationship_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='touristspot',
            name='barangay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangayApp.barangay'),
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='spot_type',
            field=models.CharField(choices=[('Natural Attraction', 'Natural Attraction'), ('Historical/Cultural Site', 'Historical/Cultural Site'), ('Adventure/Outdoor Activity', 'Adventure/Outdoor Activity'), ('Recreational/Relaxation Spot', 'Recreational/Relaxation Spot'), ('EducationalInstitution', 'Educational Institution'), ('Food/Culinary Spot', 'Food/Culinary Spot'), ('Scenic View/Lookout Point', 'Scenic View/Lookout Point'), ('Festival/Event', 'Festival/Event')], default='Natural Attraction', max_length=50),
        ),
    ]
