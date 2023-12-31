# Generated by Django 4.2.1 on 2023-11-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangayApp', '0013_transaction_barangay_transaction_municipal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='relationship',
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='spot_type',
            field=models.CharField(choices=[('Natural Attraction', 'Natural Attraction'), ('Historical/Cultural Site', 'Historical/Cultural Site'), ('Adventure/Outdoor Activity', 'Adventure/Outdoor Activity'), ('Recreational/Relaxation Spot', 'Recreational/Relaxation Spot'), ('EducationalInstitution', 'Educational Institution'), ('Food/Culinary Spot', 'Food/Culinary Spot'), ('Scenic View/Lookout Point', 'Scenic View/Lookout Point'), ('Festival/Event', 'Festival/Event')], default='Natural', max_length=50),
        ),
    ]
