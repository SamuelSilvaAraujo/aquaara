# Generated by Django 2.1.5 on 2019-03-20 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190315_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cycle',
            name='finalized',
        ),
    ]
