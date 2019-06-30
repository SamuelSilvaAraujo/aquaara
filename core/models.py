from django.template.defaultfilters import slugify
from django.db import models
from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse

from users.models import User

class Address(models.Model):
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
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    slug = models.SlugField()

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
        return (self.width*self.length*1)*1000

    def area(self):
        return self.width*self.length

    def number_cycles(self):
        return self.cycle_set.filter().count()

    def cycle(self):
        return self.cycle_set.get(despesca__isnull=True)

    def allCycle(self):
        return self.cycle_set.filter(despesca__isnull=False).order_by("-id")

class Population(models.Model):
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")
    amount_fish = models.IntegerField("Quantidade de Peixes")

class Cycle(models.Model):

    INTENSIVE = "intensive"
    SEMI_INTENSIVE = "semi-intensive"

    SYSTEM_CHOICES = [
        (INTENSIVE, 'Intensivo'),
        (SEMI_INTENSIVE, 'Semi-Intensivo')
    ]

    CONSTANT_RENEWAL = "constant-renewal"
    CONSTANT_RENEWAL_AERATORS = "constant-renewal-aerators"
    WATER_GOOD_QUALITY_HIGH_RENEWAL_AERATORS = "water-good-quality-high-renewal-aerators"

    TYPE_INTENSIVE_CHOICES = [
        (CONSTANT_RENEWAL, 'Renovação Constante'),
        (CONSTANT_RENEWAL_AERATORS, 'Renovação Constante + Aeradores'),
        (WATER_GOOD_QUALITY_HIGH_RENEWAL_AERATORS, 'Água de boa qualidade + Alta renovação + Aeradores'),
    ]

    MIDDLEWEIGHT_CHOICES = [
        (500, 500),
        (600, 600),
        (700, 700),
        (800, 800),
        (900, 900),
        (1000, 1000),
        (1100, 1100),
    ]

    DENSITY_VALUES = {
        SEMI_INTENSIVE: {500: 2.0, 600: 1.67, 700: 1.45, 800: 1.25, 900: 1.12, 1000: 1.00, 1100: 0.91},
        INTENSIVE: {
            CONSTANT_RENEWAL: {500: 4.0, 600: 3.34, 700: 2.86, 800: 2.50, 900: 2.23, 1000: 2.00, 1100: 1.82},
            CONSTANT_RENEWAL_AERATORS: {500: 6.0, 600: 5.0, 700: 4.30, 800: 3.75, 900: 3.34, 1000: 3.00, 1100: 2.73},
            WATER_GOOD_QUALITY_HIGH_RENEWAL_AERATORS: {500: 8.0, 600: 6.67, 700: 5.71, 800: 5.00, 900: 4.45, 1000: 4.00, 1100: 3.64},
        }
    }

    date = models.DateField(auto_now_add=True)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    population = models.OneToOneField(Population, on_delete=models.CASCADE, null=True, blank=True)
    system = models.CharField("Sistema", max_length=2, choices=SYSTEM_CHOICES)
    type_intensive = models.CharField("Tipo de sistema intensivo", max_length=4, choices=TYPE_INTENSIVE_CHOICES, null=True, blank=True)
    final_middleweight = models.IntegerField("Peso Médio Final", choices=MIDDLEWEIGHT_CHOICES)

    def __str__(self):
        return "{} - {}".format(self.pond.identification, self.date)

    def finalized(self):
        if self.amount_fish_current() == 0:
            return True
        return False

    def density(self):
        if self.system == self.SEMI_INTENSIVE:
            return self.DENSITY_VALUES[self.SEMI_INTENSIVE][self.final_middleweight]
        elif self.system == self.INTENSIVE:
            return self.DENSITY_VALUES[self.INTENSIVE][self.type_intensive][self.final_middleweight]

    def amount_fish_total(self):
        amount = self.density()*self.pond.area()
        return int(amount) + 1

    def amount_fish_population(self):
        return self.population.amount_fish

    def amount_fish_current(self):
        amount = self.amount_fish_population()
        mortality = self.mortality_total()
        despesca = self.despesca_total()
        return amount - mortality - despesca

    def all_mortality(self):
        return self.mortality_set.all().order_by("-id")

    def mortality_total(self):
        return self.mortality_set.all().aggregate(Sum('amount'))

    def despesca_total(self):
        return self.despesca_set.all().aggregate(Sum('amount'))

    def middleweight_current(self):
        if self.biometria_set.count() > 0:
            return self.biometria_set.all().last().middleweight
        else:
            return self.population.middleweight

    def biomassa(self):
        return (self.population.middleweight/1000) * self.amount_fish()

    def biomassa_current(self):
        return (self.middleweight_current()/1000) * self.amount_fish_current()

    def taxa_alimentar(self):
        peso_medio = self.middleweight_current()
        if self.system == 'SI':
            if 1 <= peso_medio <= 30:
                return 0.10
            elif 31 <= peso_medio <= 300:
                return 0.05
            elif 301 <= peso_medio <= 450:
                return 0.04
            elif 451 <= peso_medio <= 600:
                return 0.03
            elif 601 <= peso_medio <= 800:
                return 0.02
            elif 801 <= peso_medio <= 1100:
                return 0.01
        elif self.system == 'IN':
            if 1 <= peso_medio <= 30:
                return 0.10
            elif 31 <= peso_medio <= 100:
                return 0.07
            elif 101 <= peso_medio <= 155:
                return 0.05
            elif 156 <= peso_medio <= 450:
                return 0.04
            elif 451 <= peso_medio <= 600:
                return 0.03
            elif 601 <= peso_medio <= 800:
                return 0.02
            elif 801 <= peso_medio <= 1100:
                return 0.01

    def number_refeicoes(self):
        peso_medio = self.middleweight_current()
        if 1 <= peso_medio <= 300:
            return 4
        elif 301 <= peso_medio <= 600:
            return 3
        elif 601 <= peso_medio <= 1100:
            return 2

    def horario_refeicoes(self):
        number_refeicoes = self.number_refeicoes()
        if number_refeicoes == 4:
            return "07:00 h, 10:00 h, 13:00 h, 16:00 h"
        elif number_refeicoes == 3:
            return "07:00 h, 11:00 h, 15:00 h"
        elif number_refeicoes == 2:
            return "08:00 h, 16:00 h"

    def arracoamento(self):
        total = self.biomassa_current()*self.taxa_alimentar()
        return total/self.number_refeicoes()

    def proteina_racao(self):
        peso_medio = self.middleweight_current()
        if self.system == 'SI':
            if 1 <= peso_medio <= 100:
                return "36"
            elif 101 <= peso_medio <= 155:
                return "32 - 36"
            elif 156 <= peso_medio <= 300:
                return "32"
            elif 301 <= peso_medio <= 450:
                return "28 - 32"
            elif 451 <= peso_medio <= 1100:
                return "28"
        elif self.system == 'IN':
            if 1 <= peso_medio <= 30:
                return "40"
            elif 31 <= peso_medio <= 100:
                return "36"
            elif 101 <= peso_medio <= 155:
                return "32 - 36"
            elif 156 <= peso_medio <= 300:
                return "32"
            elif 301 <= peso_medio <= 450:
                return "28 - 32"
            elif 451 <= peso_medio <= 1100:
                return "28"

    def diametro_pelete(self):
        peso_medio = self.middleweight_current()
        if self.system == 'SI':
            if 1 <= peso_medio <= 30:
                return "1 - 2"
            elif 31 <= peso_medio <= 100:
                return "4"
            elif 101 <= peso_medio <= 155:
                return "4 - 6"
            elif 156 <= peso_medio <= 300:
                return "6"
            elif 301 <= peso_medio <= 450:
                return "6 - 8"
            elif 451 <= peso_medio <= 600:
                return "8"
            elif 601 <= peso_medio <= 800:
                return "8 - 10"
            elif 801 <= peso_medio <= 1100:
                return "10"
        elif self.system == 'IN':
            if 1 <= peso_medio <= 30:
                return "1 - 2"
            elif 31 <= peso_medio <= 100:
                return "2 - 4"
            elif 101 <= peso_medio <= 155:
                return "4 - 6"
            elif 156 <= peso_medio <= 300:
                return "6"
            elif 301 <= peso_medio <= 450:
                return "6 - 8"
            elif 451 <= peso_medio <= 600:
                return "8"
            elif 601 <= peso_medio <= 800:
                return "8 - 10"
            elif 801 <= peso_medio <= 1100:
                return "10"

    def amount_fish_biometria(self):
        amount = self.amount_fish_current()
        if amount <= 400:
            return int(amount*0.10) + 1
        elif 401 <= amount <= 700:
            return int(amount*0.07) + 1
        elif 701 <= amount <= 2000:
            return int(amount*0.05) + 1
        else:
            return int(amount*0.05) + 1

    def date_despesca(self):
        return self.population.date + timedelta(6 * 365 / 12)

    def date_biometria(self):
        if not self.biometria_set.count() > 0:
            return self.population.date + timedelta(days=15)
        else:
            biometria = self.biometria_set.all().order_by('-id')[0]
            return biometria.date + timedelta(days=15)

    def total_mortality(self):
        total = 0
        for mortality in self.all_mortality():
            total += mortality.amount
        return total

    def last_biometria(self):
        return self.biometria_set.all().order_by("-id")[0]

    def all_biometria(self):
        return self.biometria_set.all().order_by("-id")


class Mortality(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    amount = models.IntegerField("Quantidade")

class Biometria(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")

class Despesca(models.Model):
    cyle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")
    amount = models.IntegerField("Quantidade de Peixes")

class WaterQuality(models.Model):
    date = models.DateField("Data", default=datetime.now)
    transparency = models.FloatField("Transparência")
    temperature = models.FloatField("Temperatura")
    ph = models.FloatField("PH")
    oxygen = models.FloatField("Oxigênio")