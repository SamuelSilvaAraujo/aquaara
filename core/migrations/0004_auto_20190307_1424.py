# Generated by Django 2.1.5 on 2019-03-07 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_pond_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='despesca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Despesca'),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='population',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Population'),
        ),
    ]
