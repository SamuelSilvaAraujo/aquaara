from django.db import models
from datetime import datetime, timedelta
from django.db.models import Sum

from users.models import User


class Property(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Nome da Propriedade", max_length=50)
    city = models.CharField("Cidade", max_length=50)
    state = models.CharField("Estado", max_length=2, choices=STATES_CHOICES)
    district = models.CharField("Bairro/Povoado", max_length=30)
    complement = models.CharField("Complemento", max_length=100, blank=True)

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
        return (self.width * self.length * ((((self.length * 0.005) + 1) + 1) / 2)) * 1000

    def area(self):
        return self.width * self.length

    def cycle(self):
        return self.cycle_set.filter(finalized=False).first()

    def allCycle(self):
        return self.cycle_set.filter(finalized=True)

    def number_cycles(self):
        return self.allCycle().count()


class Population(models.Model):
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")
    amount_fish = models.IntegerField("Quantidade de Peixes")

    def __str__(self):
        return "{} / {}".format(self.date, self.cycle)


class WaterQuality(models.Model):
    IDEAL = 'ideal'
    ACCEPTABLE = 'acceptable'
    BAD = 'bad'
    TERRIBLE = 'terrible'

    QUALITY_CHOICES = {
        IDEAL, 'Ideal',
        ACCEPTABLE, 'Aceitável',
        BAD, 'Ruim',
        TERRIBLE, 'Terrível'
    }

    date = models.DateField("Data", default=datetime.now)
    transparency = models.FloatField("Transparência")
    temperature = models.FloatField("Temperatura")
    ph = models.FloatField("PH")
    oxygen = models.FloatField("Oxigênio")

    def quality(self):
        if self.transparency == 40 and (25 <= self.temperature <= 27) and (6.5 <= self.ph <= 8.4) and self.oxygen == 5:
            return self.IDEAL
        elif (30 <= self.transparency <= 50) and (20 <= self.temperature <= 32) and (4.5 <= self.ph <= 8.0) and (
                3 <= self.oxygen <= 5):
            return self.ACCEPTABLE
        elif (self.transparency == 25 or self.transparency == 60) and (
                self.temperature <= 20 or self.temperature >= 32) and (self.ph <= 4.5 or self.ph >= 8.0) and (
                2 <= self.oxygen <= 3 or 5 <= self.oxygen <= 7):
            return self.BAD
        elif (self.transparency <= 25 or self.transparency >= 60) and (
                self.temperature <= 20 or self.temperature >= 32) and (self.ph <= 4.5 or self.ph >= 8.0) and (
                self.oxygen == 1 or self.oxygen == 7):
            return self.TERRIBLE
        else:
            return None

    def water_renovation(self):
        if self.quality() == self.IDEAL:
            return "1%"
        elif self.quality() == self.ACCEPTABLE:
            return "1 a 5%"
        elif self.quality() == self.BAD:
            return "10 a 20%"
        elif self.quality() == self.TERRIBLE:
            return "Renovação constante"


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
            WATER_GOOD_QUALITY_HIGH_RENEWAL_AERATORS: {500: 8.0, 600: 6.67, 700: 5.71, 800: 5.00, 900: 4.45, 1000: 4.00,
                                                       1100: 3.64},
        }
    }

    date = models.DateField(auto_now_add=True)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    population = models.OneToOneField(Population, on_delete=models.CASCADE, null=True, blank=True)
    water_quality = models.OneToOneField(WaterQuality, on_delete=models.CASCADE, null=True, blank=True)
    system = models.CharField("Sistema", max_length=15, choices=SYSTEM_CHOICES)
    type_intensive = models.CharField("Tipo de sistema intensivo", max_length=50, choices=TYPE_INTENSIVE_CHOICES,
                                      null=True, blank=True)
    final_middleweight = models.IntegerField("Peso Médio Final", choices=MIDDLEWEIGHT_CHOICES)
    finalized = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "{} - {}".format(self.pond.identification, self.date)

    def density(self):
        if self.system == self.SEMI_INTENSIVE:
            return self.DENSITY_VALUES[self.SEMI_INTENSIVE][self.final_middleweight]
        elif self.system == self.INTENSIVE:
            return self.DENSITY_VALUES[self.INTENSIVE][self.type_intensive][self.final_middleweight]

    # quantidade de peixes

    def amount_fish_total(self):
        amount = self.density() * self.pond.area()
        return amount

    def amount_fish_population(self):
        return self.population.amount_fish

    def amount_fish_current(self):
        amount = self.amount_fish_population()
        mortality = self.mortality_total()
        despesca = self.despesca_total()
        return amount - mortality - despesca

    def amount_fish_period(self, date):
        total_amount = self.amount_fish_population()
        mortality = self.mortality_total_period(date)
        despesca = self.despesca_total_period(date)
        return total_amount - mortality - despesca

    # mortalidade

    def all_mortality(self):
        return self.mortality_set.all()

    def mortality_total(self):
        return self.all_mortality().aggregate(Sum('amount')).get('amount__sum') or 0

    def mortality_total_period(self, date):
        return self.all_mortality().filter(date__lt=date).aggregate(Sum('amount')).get('amount__sum') or 0

    # despesca

    def all_despesca(self):
        return self.despesca_set.all()

    def despesca_total(self):
        return self.all_despesca().aggregate(Sum('amount')).get('amount__sum') or 0

    def despesca_total_period(self, date):
        return self.all_despesca().filter(date__lt=date).aggregate(Sum('amount')).get('amount__sum') or 0

    def last_despesca(self):
        return self.all_despesca().first()

    # peso médio

    def population_middleweight(self):
        return self.population.middleweight

    def current_middleweight(self):
        return self.all_biometria().first().middleweight if self.all_biometria().count() > 0 else self.population_middleweight()

    def period_middleweight(self):
        list = [{
            'date': self.population.date,
            'value': self.population_middleweight()
        }]
        biometrias = self.all_biometria()

        for biometria in biometrias:
            middleweight = {
                'date': biometria.date,
                'value': biometria.middleweight
            }
            list.append(middleweight)
        return list

    def last_middleweight(self):
        return self.all_despesca().first().middleweight

    # biomassa

    def biomassa(self, middleweight, amount_fish):
        return (middleweight / 1000) * amount_fish

    def first_biomassa(self):
        return self.biomassa(self.population_middleweight(), self.amount_fish_population())

    def max_biomassa(self):
        return self.biomassa(self.current_middleweight(), self.amount_fish_total())

    def current_biomassa(self):
        return self.biomassa(self.current_middleweight(), self.amount_fish_current())

    def last_biomassa(self):
        return self.biomassa(self.last_middleweight(), self.amount_fish_period(self.last_despesca().date))

    # arraçoamento

    def feed_rate(self, middleweight):
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

    def meal_times(self):
        number_feeds = self.number_feeds()
        if number_feeds == 4:
            return "07:00 h, 10:00 h, 13:00 h, 16:00 h"
        elif number_feeds == 3:
            return "07:00 h, 11:00 h, 15:00 h"
        elif number_feeds == 2:
            return "08:00 h, 16:00 h"

    def full_day_feeding(self):
        return self.current_biomassa() * self.feed_rate(self.current_middleweight())

    def feeding_meal(self):
        return self.full_day_feeding() / self.number_feeds()

    def proteina_racao(self):
        middleweight = self.current_middleweight()
        if self.system == self.SEMI_INTENSIVE:
            if 1 <= middleweight <= 100:
                return "36 %"
            elif 101 <= middleweight <= 155:
                return "32 - 36 %"
            elif 156 <= middleweight <= 300:
                return "32 %"
            elif 301 <= middleweight <= 450:
                return "28 - 32 %"
            elif 451 <= middleweight <= 1100:
                return "28 %"
        elif self.system == self.INTENSIVE:
            if 1 <= middleweight <= 30:
                return "40 %"
            elif 31 <= middleweight <= 100:
                return "36 %"
            elif 101 <= middleweight <= 155:
                return "32 - 36 %"
            elif 156 <= middleweight <= 300:
                return "32 %"
            elif 301 <= middleweight <= 450:
                return "28 - 32 %"
            elif 451 <= middleweight <= 1100:
                return "28 %"

    def diametro_pelete(self):
        middleweight = self.current_middleweight()
        if self.system == self.SEMI_INTENSIVE:
            if 1 <= middleweight <= 30:
                return "1 - 2 mm"
            elif 31 <= middleweight <= 100:
                return "4 mm"
            elif 101 <= middleweight <= 155:
                return "4 - 6 mm"
            elif 156 <= middleweight <= 300:
                return "6 mm"
            elif 301 <= middleweight <= 450:
                return "6 - 8 mm"
            elif 451 <= middleweight <= 600:
                return "8 mm"
            elif 601 <= middleweight <= 800:
                return "8 - 10 mm"
            elif 801 <= middleweight <= 1100:
                return "10 mm"
        elif self.system == self.INTENSIVE:
            if 1 <= middleweight <= 30:
                return "1 - 2 mm"
            elif 31 <= middleweight <= 100:
                return "2 - 4 mm"
            elif 101 <= middleweight <= 155:
                return "4 - 6 mm"
            elif 156 <= middleweight <= 300:
                return "6 mm"
            elif 301 <= middleweight <= 450:
                return "6 - 8 mm"
            elif 451 <= middleweight <= 600:
                return "8 mm"
            elif 601 <= middleweight <= 800:
                return "8 - 10 mm"
            elif 801 <= middleweight <= 1100:
                return "10 mm"

    # biometria

    def amount_fish_next_biometria(self):
        amount = self.amount_fish_current()
        if amount <= 400:
            return amount * 0.10
        elif 401 <= amount <= 700:
            return amount * 0.07
        elif 701 <= amount <= 2000:
            return amount * 0.05
        else:
            return amount * 0.03

    def date_next_biometria(self):
        td = timedelta(days=15)
        return self.biometria_set.first().date + td if self.biometria_set.count() > 0 else self.population.date + td

    def all_biometria(self):
        return self.biometria_set.all()

    # custo e conversão alimentar

    def ration_total(self):
        total_ration = 0

        all_biometria = self.all_biometria().order_by('date')

        start_date = self.population.date

        if self.all_biometria().count() > 0:
            end_date = all_biometria.first().date
        else:
            end_date = datetime.now().date()

        population_middleweight = self.population_middleweight()
        amount_fish_population = self.amount_fish_population()
        population_biomassa = self.biomassa(population_middleweight, amount_fish_population)

        ration = population_biomassa * self.feed_rate(population_middleweight)
        number_days = (end_date - start_date).days
        total_ration += ration * number_days

        for biometria in all_biometria:
            start_date = biometria.date

            next_biometria = all_biometria.filter(date__gt=start_date).first()
            if next_biometria:
                end_date = next_biometria.date
            else:
                end_date = datetime.now().date()

            biometria_middleweight = biometria.middleweight
            biometria_amount_fish = self.amount_fish_period(biometria.date)
            biometria_biomassa = self.biomassa(biometria_middleweight, biometria_amount_fish)

            ration = biometria_biomassa * self.feed_rate(biometria_middleweight)
            number_days = (end_date - start_date).days
            total_ration += ration * number_days

        return total_ration

    def food_conversion(self):
        biomassa = self.current_biomassa() - self.first_biomassa()
        if biomassa > 0:
            return self.ration_total() / biomassa
        else:
            return 0

    def final_food_conversion(self):
        biomassa = self.last_biomassa() - self.first_biomassa()
        return self.ration_total() / biomassa

    def cost_total(self):
        cost_dict = {
            'total': 0,
            'periods': []
        }

        all_biometria = self.all_biometria().order_by('date')

        start_date = self.population.date

        if self.all_biometria().count() > 0:
            end_date = all_biometria.first().date
        else:
            end_date = datetime.now().date()

        population_middleweight = self.population_middleweight()
        amount_fish_population = self.amount_fish_population()
        population_biomassa = self.biomassa(population_middleweight, amount_fish_population)

        ration = population_biomassa * self.feed_rate(population_middleweight)
        number_days = (end_date - start_date).days

        total_ration = ration * number_days

        cost = self.all_cost().filter(date__lte=start_date).first()

        value = total_ration * cost.price_kg()

        cost_dict['total'] += value
        cost_dict['periods'].append({
            'start_date': start_date,
            'end_date': end_date,
            'value': value
        })

        for biometria in all_biometria:
            start_date = biometria.date

            next_biometria = all_biometria.filter(date__gt=start_date).first()
            if next_biometria:
                end_date = next_biometria.date
            else:
                end_date = datetime.now().date()

            biometria_middleweight = biometria.middleweight
            biometria_amount_fish = self.amount_fish_period(biometria.date)
            biometria_biomassa = self.biomassa(biometria_middleweight, biometria_amount_fish)

            ration = biometria_biomassa * self.feed_rate(biometria_middleweight)
            number_days = (end_date - start_date).days
            total_ration = ration * number_days

            cost = self.all_cost().filter(date__lte=start_date).first()

            value = total_ration * cost.price_kg()

            cost_dict['total'] += value
            cost_dict['periods'].append({
                'start_date': start_date,
                'end_date': end_date,
                'value': value
            })

        return cost_dict

    def all_cost(self):
        return self.cost_set.all()


class Mortality(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    amount = models.IntegerField("Quantidade")

    class Meta:
        ordering = ['-date']


class Biometria(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio", null=True, blank=True)

    class Meta:
        ordering = ['-date']


class Despesca(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Médio")
    amount = models.IntegerField("Quantidade de Peixes")

    class Meta:
        ordering = ['-date']


class Cost(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField("Preço")
    weight = models.FloatField("Peso")

    class Meta:
        ordering = ['-date']

    def price_kg(self):
        return self.price / self.weight
