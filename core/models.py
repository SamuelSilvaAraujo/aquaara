from django.template.defaultfilters import slugify
from django.db import models
from datetime import datetime, timedelta
from django.db.models import Sum, Q
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

    def __str__(self):
        return "{}-{}".format(self.city, self.state)

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

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

    class Meta:
        ordering = ['-date']

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

    def amount_fish_period(self, end_date):
        total_amount = self.amount_fish_population()
        mortality = self.all_mortality().filter(date__lte=end_date).aggregate(Sum('amount')).get('amount__sum') or 0
        despesca = self.all_despesca().filter(date__lte=end_date).aggregate(Sum('amount')).get('amount__sum') or 0
        return total_amount - mortality - despesca

    def all_mortality(self):
        return self.mortality_set.all()

    def mortality_total(self):
        return self.all_mortality().aggregate(Sum('amount')).get('amount__sum') or 0

    def all_despesca(self):
        return self.despesca_set.all()

    def despesca_total(self):
        return self.all_despesca().aggregate(Sum('amount')).get('amount__sum') or 0

    def population_middleweight(self):
        return self.population.middleweight

    def current_middleweight(self):
        return self.all_biometria().first().middleweight if self.all_biometria().count() > 0 else self.population_middleweight()

    def period_middleweight(self, end_data):
        biometria = self.all_biometria().filter(date__lte=end_data)
        return biometria.first().middleweight if biometria.count() > 0 else self.population_middleweight()

    def first_biomassa(self):
        return (self.population_middleweight()/1000) * self.amount_fish_population()

    def max_biomassa(self):
        return (self.current_middleweight()/1000) * self.amount_fish_total()

    def current_biomassa(self):
        return (self.current_middleweight()/1000) * self.amount_fish_current()

    def period_biomassa(self, middleweight, amount_fish):
        return (middleweight/1000) * amount_fish

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
        return self.current_biomassa()*self.feed_rate(self.current_middleweight())

    def feeding_meal(self):
        return self.full_day_feeding()/self.number_feeds()

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

    def amount_fish_biometria(self):
        amount = self.amount_fish_current()
        if amount <= 400:
            return amount*0.10
        elif 401 <= amount <= 700:
            return amount*0.07
        elif 701 <= amount <= 2000:
            return amount*0.05
        else:
            return amount*0.03

    def date_next_biometria(self):
        td = timedelta(days=15)
        return self.biometria_set.first().date + td if self.biometria_set.count() > 0 else self.population.date + td

    def all_biometria(self):
        return self.biometria_set.all()

    def current_cost(self):
        return self.cost_set.last()

    # def period_feeding(self, middleweight, start_date, end_date):
    #     number_days = end_date - start_date
    #     amount_fish = self.period_amount_fish(end_date)
    #     biomassa = self.period_biomassa(middleweight, amount_fish)
    #     feeding = biomassa * self.feed_rate(middleweight)
    #     return feeding*number_days.days

    def ration_total(self, start_date, end_date):
        period_mortality = [m for m in self.all_mortality().filter(Q(date__gte=start_date) & Q(date__lte=end_date)).values_list("date", flat=True)]
        period_despesca = [d for d in self.all_despesca().filter(Q(date__gte=start_date) & Q(date__lte=end_date)).values_list("date", flat=True)]
        dates_list = set(period_mortality + period_despesca)
        total_ration = 0

        if len(dates_list) > 0:
            for date in dates_list:
                number_days = (start_date - date).days
                middleweight = self.period_middleweight(date)
                amount_fish = self.amount_fish_period(date)
                biomassa = (middleweight / 1000) * amount_fish
                feeding = biomassa * self.feed_rate(middleweight)
                total_ration += feeding * number_days
                start_date = date

            number_days = (start_date - end_date).days
            middleweight = self.period_middleweight(end_date)
            amount_fish = self.amount_fish_period(end_date)
            biomassa = (middleweight / 1000) * amount_fish
            feeding = biomassa * self.feed_rate(middleweight)
            total_ration += feeding * number_days

        else:
            number_days = (start_date - end_date).days
            middleweight = self.period_middleweight(end_date)
            amount_fish = self.amount_fish_period(end_date)
            biomassa = (middleweight / 1000) * amount_fish
            feeding = biomassa * self.feed_rate(middleweight)
            total_ration += feeding * number_days

        return total_ration

    def food_conversion(self):
        biomassa = self.current_biomassa() - self.first_biomassa()
        ration_total = self.ration_total(self.population.date, datetime.now().date())
        return ration_total/biomassa or 0

    def cost_period(self,feeding, start_date, end_date):
        cost = self.cost_set.filter(Q(date__gte=start_date) & Q(date__lt=end_date))
        return 0

    def periods(self):
        list = []
        start_date = self.population.date
        middleweight = self.population.middleweight
        # for biometria in self.all_biometria():
        #     end_date = biometria.date
        #     period_mortality = [m for m in self.all_mortality().filter(Q(date__gte=start_date) & Q(date__lte=end_date)).values_list("date", flat=True)]
        #     period_despesca = [d for d in self.all_despesca().filter(Q(date__gte=start_date) & Q(date__lte=end_date)).values_list("date", flat=True)]
        #     dates_list = set(period_mortality + period_despesca)
        #     feeding = 0
        #     start_date_period = start_date
        #     if len(dates_list) > 0:
        #         for date in dates_list:
        #             feeding += self.period_feeding(middleweight, start_date_period, date)
        #             start_date_period = date
        #         feeding += self.period_feeding(middleweight, start_date_period, end_date)
        #     else:
        #         feeding += self.period_feeding(middleweight, start_date, end_date)
        #
        #     cost = self.cost_period(feeding, start_date, end_date)
        #     # food_conversion = self.food_conversion(feeding, middleweight, biometria.middleweight, start_date, end_date)
        #     list.append({
        #         "period": {"start": start_date, "end": end_date},
        #         # "food_conversion": food_conversion,
        #         "cost": cost
        #     })
        #     start_date = end_date
        #     middleweight = biometria.middleweight
        return list


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
        ordering = ['-date']

    def price_kg(self):
        return self.price/self.weight