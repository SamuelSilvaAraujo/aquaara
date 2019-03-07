# Generated by Django 2.1.5 on 2019-03-07 12:34

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
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20, verbose_name='Cidade')),
                ('district', models.CharField(max_length=30, verbose_name='Bairro')),
                ('number', models.IntegerField(verbose_name='Numero')),
                ('street', models.CharField(max_length=30, verbose_name='Rua')),
                ('state', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Biometria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('middleweight', models.FloatField(verbose_name='Peso Medio')),
                ('mortality', models.IntegerField(verbose_name='Mortalidade')),
            ],
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_system', models.CharField(choices=[('IN', 'Intensivo'), ('SI', 'Semi-Intensivo')], max_length=2, verbose_name='Tipo de Sistema')),
                ('middleweight_despesca', models.FloatField(verbose_name='Peso Medio Esperado na Despeca')),
                ('finalized', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Despesca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('final_middleweight', models.FloatField(verbose_name='Peso Medio Final')),
                ('final_amount', models.IntegerField(verbose_name='Quantidade Final de peixes')),
            ],
        ),
        migrations.CreateModel(
            name='Pond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.CharField(max_length=20, unique=True, verbose_name='Identificação')),
                ('width', models.IntegerField(verbose_name='Largura')),
                ('length', models.IntegerField(verbose_name='Comprimento')),
                ('water_flow', models.FloatField(verbose_name='Vazão de Água')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('middleweight', models.FloatField(verbose_name='Peso Medio')),
                ('amount', models.IntegerField(verbose_name='Quantidade de peixes')),
                ('age', models.FloatField(verbose_name='Idade do peixe')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('slug', models.SlugField(unique=True)),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Adress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pond',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Property'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='despesca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Despesca'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='pond',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pond'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='population',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Population'),
        ),
        migrations.AddField(
            model_name='biometria',
            name='ciclo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cycle'),
        ),
    ]
