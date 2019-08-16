# Generated by Django 2.1.5 on 2019-07-19 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterquality',
            name='cycle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Cycle'),
            preserve_default=False,
        ),
    ]
