# Generated by Django 2.1.5 on 2019-03-07 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, verbose_name='CPF'),
        ),
    ]
