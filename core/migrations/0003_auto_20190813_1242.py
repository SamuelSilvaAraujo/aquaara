# Generated by Django 2.1.5 on 2019-08-13 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_waterquality_cycle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterquality',
            name='cycle',
        ),
        migrations.AddField(
            model_name='cycle',
            name='water_quality',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.WaterQuality'),
        ),
    ]
