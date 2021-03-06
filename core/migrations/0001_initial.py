# Generated by Django 2.1.5 on 2019-07-18 17:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Biometria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('middleweight', models.FloatField(blank=True, null=True, verbose_name='Peso Médio')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('price', models.FloatField(verbose_name='Preço')),
                ('weight', models.FloatField(verbose_name='Peso')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('system', models.CharField(choices=[('intensive', 'Intensivo'), ('semi-intensive', 'Semi-Intensivo')], max_length=15, verbose_name='Sistema')),
                ('type_intensive', models.CharField(blank=True, choices=[('constant-renewal', 'Renovação Constante'), ('constant-renewal-aerators', 'Renovação Constante + Aeradores'), ('water-good-quality-high-renewal-aerators', 'Água de boa qualidade + Alta renovação + Aeradores')], max_length=50, null=True, verbose_name='Tipo de sistema intensivo')),
                ('final_middleweight', models.IntegerField(choices=[(500, 500), (600, 600), (700, 700), (800, 800), (900, 900), (1000, 1000), (1100, 1100)], verbose_name='Peso Médio Final')),
                ('finalized', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Despesca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('middleweight', models.FloatField(verbose_name='Peso Médio')),
                ('amount', models.IntegerField(verbose_name='Quantidade de Peixes')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cycle')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Mortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('amount', models.IntegerField(verbose_name='Quantidade')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cycle')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Pond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.CharField(max_length=20, verbose_name='Identificação')),
                ('width', models.FloatField(verbose_name='Largura')),
                ('length', models.FloatField(verbose_name='Comprimento')),
                ('water_flow', models.FloatField(verbose_name='Vazão de Água')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('middleweight', models.FloatField(verbose_name='Peso Médio')),
                ('amount_fish', models.IntegerField(verbose_name='Quantidade de Peixes')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome da Propriedade')),
                ('city', models.CharField(max_length=50, verbose_name='Cidade')),
                ('state', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
                ('district', models.CharField(max_length=30, verbose_name='Bairro/Povoado')),
                ('complement', models.CharField(blank=True, max_length=100, verbose_name='Complemento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaterQuality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Data')),
                ('transparency', models.FloatField(verbose_name='Transparência')),
                ('temperature', models.FloatField(verbose_name='Temperatura')),
                ('ph', models.FloatField(verbose_name='PH')),
                ('oxygen', models.FloatField(verbose_name='Oxigênio')),
            ],
        ),
        migrations.AddField(
            model_name='pond',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Property'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='pond',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pond'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='population',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Population'),
        ),
        migrations.AddField(
            model_name='cost',
            name='cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cycle'),
        ),
        migrations.AddField(
            model_name='biometria',
            name='cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cycle'),
        ),
    ]
