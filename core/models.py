from django.template.defaultfilters import slugify
from django.db import models
from datetime import datetime, timedelta

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
        return (self.width*self.length*1)*1000

    def area(self):
        return self.width*self.length

    def number_cycles(self):
        return self.cycle_set.filter(finalized=True).count()

    def cycle(self):
        return self.cycle_set.filter(finalized=False).first()

    def allCycle(self):
        return self.cycle_set.filter(finalized=True)

class Population(models.Model):
    date = models.DateField("Data", default=datetime.now)
    middleweight = models.FloatField("Peso Medio")

class Despesca(models.Model):
    date = models.DateField("Data")
    final_middleweight = models.FloatField("Peso Medio Final")

class Cycle(models.Model):
    SYSTEM_CHOICES = [
        ('IN', 'Intensivo'),
        ('SI', 'Semi-Intensivo')
    ]

    TYPE_INTENSIVE = [
        ('RC', 'Renovação Constante'),
        ('RCA', 'Renovação Constante + Aeradores'),
        ('ABAA', 'Água de boa qualidade + Alta renovação + Aeradores'),
    ]

    MIDDLEWEIGHT = [
        (0.500, '0.500'),
        (0.600, '0.600'),
        (0.700, '0.700'),
        (0.800, '0.800'),
        (0.900, '0.900'),
        (1.000, '1.000'),
        (1.100, '1.100'),
    ]

    densidade = {
        'SI': {0.500: 2.0, 0.600: 1.67, 0.700: 1.45, 0.800: 1.25, 0.900: 1.12, 1.000: 1.00, 1.100: 0.91},
        'IN': {
            'RC': {0.500: 4.0, 0.600: 3.34, 0.700: 2.86, 0.800: 2.50, 0.900: 2.23, 1.000: 2.00, 1.100: 1.82},
            'RCA': {0.500: 6.0, 0.600: 5.0, 0.700: 4.30, 0.800: 3.75, 0.900: 3.34, 1.000: 3.00, 1.100: 2.73},
            'ABAA': {0.500: 8.0, 0.600: 6.67, 0.700: 5.71, 0.800: 5.00, 0.900: 4.45, 1.000: 4.00, 1.100: 3.64},
        }
    }

    date = models.DateField(auto_now_add=True)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    population = models.ForeignKey(Population, on_delete=models.CASCADE, null=True, blank=True)
    despesca = models.ForeignKey(Despesca, on_delete=models.CASCADE, null=True, blank=True)
    system = models.CharField("Sistema", max_length=2, choices=SYSTEM_CHOICES)
    type_intensive = models.CharField("Tipo de sistema intensivo", max_length=4, choices=TYPE_INTENSIVE, null=True, blank=True)
    middleweight_despesca = models.FloatField("Peso Medio estimado para a Despeca", choices=MIDDLEWEIGHT)
    finalized = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.pond.identification, self.date)

    def density(self):
        if self.system == 'SI':
            return self.densidade['SI'][self.middleweight_despesca]
        elif self.system == 'IN':
            return self.densidade['IN'][self.type_intensive][self.middleweight_despesca]

    def amount_fish(self):
        amount = self.density()*self.pond.area()
        for mortality in self.mortality_set.all():
            amount -= mortality.amount
        return amount

    def peso_medio(self):
        if self.population:
            if self.biometria_set.count() > 0:
                biometria = self.biometria_set.all().order_by('date')[0]
                return biometria.middleweight
            else:
                return self.population.middleweight
        else:
            return None

    def biomassa(self):
        if self.population:
            return self.peso_medio() * self.amount_fish()
        else:
            return None

    def taxa_alimentar(self):
        peso_medio = self.peso_medio()
        if self.system == 'SI':
            if 1 <= peso_medio <= 30:
                return 0.10
            elif 31 <= peso_medio <= 300:
                return 0.5
            elif 301 <= peso_medio <= 450:
                return 0.4
            elif 451 <= peso_medio <= 600:
                return 0.3
            elif 601 <= peso_medio <= 800:
                return 0.2
            elif 801 <= peso_medio <= 1100:
                return 0.1
        elif self.system == 'IN':
            if 1 <= peso_medio <= 30:
                return 0.10
            elif 31 <= peso_medio <= 100:
                return 0.7
            elif 101 <= peso_medio <= 155:
                return 0.5
            elif 156 <= peso_medio <= 450:
                return 0.4
            elif 451 <= peso_medio <= 600:
                return 0.3
            elif 601 <= peso_medio <= 800:
                return 0.2
            elif 801 <= peso_medio <= 1100:
                return 0.1

    def number_refeicoes(self):
        peso_medio = self.peso_medio()
        if 1 <= peso_medio <= 300:
            return 4
        elif 301 <= peso_medio <= 600:
            return 3
        elif 601 <= peso_medio <= 1100:
            return 2

    def horario_refeicoes(self):
        number_refeicoes = self.number_refeicoes()
        if number_refeicoes == 4:
            return "07:00, 11:00, 14:00, 17:00"
        elif number_refeicoes == 3:
            return "07:00, 12:00, 17:00"

    def arracoamento(self):
        return (self.amount_fish()*self.peso_medio()*self.taxa_alimentar())/100

    def proteina_racao(self):
        peso_medio = self.peso_medio()
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
        peso_medio = self.peso_medio()
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
            if not self.biometria_set.count() > 0:
                return self.population.date + timedelta(days=15)
            else:
                biometria = self.biometria_set.all().order_by('date')[0]
                return biometria.date + timedelta(days=15)

class Mortality(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data", default=datetime.now)
    amount = models.IntegerField("Quantidade")

class Biometria(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField("Data")
    middleweight = models.FloatField("Peso Medio")

    def quant_peixe(self):
        amount_fish = self.cycle.amount_fish()
        if amount_fish <= 400:
            return 0.10
        elif 401 <= amount_fish <= 700:
            return 0.7
        elif 701 <= amount_fish <= 2000:
            return 0.5

class WaterQuality(models.Model):
    date = models.DateField("Data", default=datetime.now)
    transparency = models.FloatField("Transparência")
    temperature = models.FloatField("Temperatura")
    ph = models.FloatField("PH")
    oxygen = models.FloatField("Oxigênio")