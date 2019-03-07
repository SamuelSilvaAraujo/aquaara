from django.template.defaultfilters import slugify
from django.db import models
from datetime import datetime, timedelta

from users.models import User

class Adress(models.Model):
    STATES_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]

    city = models.CharField("Cidade", max_length=20)
    district = models.CharField("Bairro", max_length=30)
    number = models.IntegerField("Numero")
    street = models.CharField("Rua", max_length=30)
    state = models.CharField("Estado", choices=STATES_CHOICES, max_length=2)

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=50)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Property, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Pond(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    identification = models.CharField("Identificação", max_length=20)
    width = models.IntegerField("Largura")
    length = models.IntegerField("Comprimento")
    water_flow = models.FloatField("Vazão de Água")

    def __str__(self):
        return self.identification

    def volume(self):
        return self.width*self.length*1

    def area(self):
        return self.width*self.length

    def number_cycles(self):
        return self.cycle_set.count()

    def cycle(self):
        return self.cycle_set.filter(finalized=False).first()

class Population(models.Model):
    date = models.DateField("Data")
    middleweight = models.FloatField("Peso Medio")
    amount = models.IntegerField("Quantidade de peixes")
    age = models.FloatField("Idade do peixe")

class Despesca(models.Model):
    date = models.DateField("Data")
    final_middleweight = models.FloatField("Peso Medio Final")
    final_amount = models.IntegerField("Quantidade Final de peixes")

class Cycle(models.Model):
    TYPE_SYSTEM_CHOICES = [
        ('IN', 'Intensivo'),
        ('SI', 'Semi-Intensivo')
    ]

    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    population = models.ForeignKey(Population, on_delete=models.CASCADE, null=True, blank=True)
    despesca = models.ForeignKey(Despesca, on_delete=models.CASCADE, null=True, blank=True)
    type_system = models.CharField("Tipo de Sistema", max_length=2, choices=TYPE_SYSTEM_CHOICES)
    middleweight_despesca = models.FloatField("Peso Medio Esperado na Despeca")
    finalized = models.BooleanField(default=False)

    def date_despesca(self):
        if not self.population:
            return None
        else:
            date_population = self.population.date
            return date_population + timedelta(6*365/12)

    def date_biometria(self):
        if not self.population:
            return None
        else:
            biometrias = self.biometria_set.all().order_by('date')
            if not len(biometrias) > 0:
                return self.population.date + timedelta(days=15)
            else:
                return biometrias[0].date + timedelta(days=15)

class Biometria(models.Model):
    ciclo = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data")
    middleweight = models.FloatField("Peso Medio")
    mortality = models.IntegerField("Mortalidade")