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
    width = models.FloatField("Largura")
    length = models.FloatField("Comprimento")
    water_flow = models.FloatField("Vazão de Água")

    def __str__(self):
        return self.identification

    def volume(self):
        return (self.width*self.length*1)*1000

    def area(self):
        return self.width*self.length

    def cycle(self):
        return self.cycle_set.get(finalized=False)

    def allCycle(self):
        return self.cycle_set.filter(finalized=True).order_by("date")

    def number_cycles(self):
        return self.allCycle().count()

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
    system = models.CharField("Sistema", max_length=15, choices=SYSTEM_CHOICES)
    type_intensive = models.CharField("Tipo de sistema intensivo", max_length=50, choices=TYPE_INTENSIVE_CHOICES, null=True, blank=True)
    final_middleweight = models.IntegerField("Peso Médio Final", choices=MIDDLEWEIGHT_CHOICES)
    finalized = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.pond.identification, self.date)

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

    def previous_amount_fish(self):
        last_biometria = self.biometria_set.last()
        total_amount = self.amount_fish_population()
        total_mortality = self.all_mortality().filter(date__lt=last_biometria.date)
        total_despesca = self.all_despesca().filter(date__lt=last_biometria.date)
        return total_amount - total_mortality - total_despesca

    def all_mortality(self):
        return self.mortality_set.all()

    def mortality_total(self):
        all_mortality = self.all_mortality()
        if len(all_mortality) > 0:
            return all_mortality.aggregate(Sum('amount')).get('amount__sum')
        return 0

    def all_despesca(self):
        return self.despesca_set.all()

    def despesca_total(self):
        all_despesca = self.all_despesca()
        if len(all_despesca) > 0:
            return all_despesca.aggregate(Sum('amount')).get('amount__sum')
        return 0

    def population_middleweight(self):
        return self.population.middleweight

    def current_middleweight(self):
        return self.biometria_set.last().middleweight if self.biometria_set.last() else self.population_middleweight()

    def previous_middleweight(self):
        return self.biometria_set.all()[1].middleweight if self.biometria_set.count() > 1 else self.population_middleweight()

    def biomassa(self):
        return (self.current_middleweight()/1000) * self.amount_fish_total()

    def current_biomassa(self):
        return (self.current_middleweight()/1000) * self.amount_fish_current()

    def previous_biomassa(self):
        return (self.previous_middleweight()/1000) * self.previous_amount_fish()

    def feed_rate(self, middleweight):
        # peso_medio = self.current_middleweight()
        if self.system == self.SEMI_INTENSIVE:
            if 1 <= middleweight <= 30:
                return 0.10
            elif 31 <= middleweight <= 300:
                return 0.05
            elif 301 <= middleweight <= 450:
                return 0.04
            elif 451 <= middleweight <= 600:
                return 0.03
            elif 601 <= middleweight <= 800:
                return 0.02
            elif 801 <= middleweight <= 1100:
                return 0.01
        elif self.system == self.INTENSIVE:
            if 1 <= middleweight <= 30:
                return 0.10
            elif 31 <= middleweight <= 100:
                return 0.07
            elif 101 <= middleweight <= 155:
                return 0.05
            elif 156 <= middleweight <= 450:
                return 0.04
            elif 451 <= middleweight <= 600:
                return 0.03
            elif 601 <= middleweight <= 800:
                return 0.02
            elif 801 <= middleweight <= 1100:
                return 0.01

    def number_feeds(self):
        middleweight = self.current_middleweight()
        if 1 <= middleweight <= 300:
            return 4
        elif 301 <= middleweight <= 600:
            return 3
        elif 601 <= middleweight <= 1100:
            return 2

    def horario_refeicoes(self):
        number_feeds = self.number_feeds()
        if number_feeds == 4:
            return "07:00 h, 10:00 h, 13:00 h, 16:00 h"
        elif number_feeds == 3:
            return "07:00 h, 11:00 h, 15:00 h"
        elif number_feeds == 2:
            return "08:00 h, 16:00 h"

    def full_day_feeding(self):
        return self.current_biomassa()*self.feed_rate(self.current_middleweight())

    def feed_meal(self):
        return self.full_day_feeding()/self.number_feeds()

    def full_period_feeding(self):
        last_date = self.population.date
        for biometria in self.all_biometria():
            pass
        return

    def proteina_racao(self):
        peso_medio = self.current_middleweight()
        if self.system == self.SEMI_INTENSIVE:
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
        elif self.system == self.INTENSIVE:
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
        peso_medio = self.current_middleweight()
        if self.system == self.SEMI_INTENSIVE:
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
        elif self.system == self.INTENSIVE:
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

    def last_biometria(self):
        return self.biometria_set.last()

    def all_biometria(self):
        return self.biometria_set.all()

    def current_cost(self):
        return self.cost_set.last()

class Mortality(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    amount = models.IntegerField("Quantidade")

    class Meta:
        ordering = ['date']

class Biometria(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")

    class Meta:
        ordering = ['date']

class Despesca(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")
    amount = models.IntegerField("Quantidade de Peixes")

    class Meta:
        ordering = ['date']

class WaterQuality(models.Model):
    date = models.DateField("Data", default=datetime.now)
    transparency = models.FloatField("Transparência")
    temperature = models.FloatField("Temperatura")
    ph = models.FloatField("PH")
    oxygen = models.FloatField("Oxigênio")

class Cost(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField("Preço")
    weight = models.FloatField("Peso")

    class Meta:
        ordering = ['date']