# Generated by Django 2.1.5 on 2019-03-07 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190307_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pond',
            name='slug',
        ),
    ]
