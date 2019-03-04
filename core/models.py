from django.template.defaultfilters import slugify
from django.db import models

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
    identification = models.CharField("Identificação", max_length=20, unique=True)
    width = models.IntegerField("Largura")
    length = models.IntegerField("Comprimento")
    quant_povoamento = models.IntegerField(default=0)
    vazao = models.FloatField("Vazão")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.identification

    def save(self, *args, **kwargs):
        self.slug = slugify(self.identification)
        super(Pond, self).save(*args, **kwargs)

    def volume(self):
        return self.width*self.length*1

    def area(self):
        return self.width*self.length

class Population(models.Model):

    TYPE_SYSTEM_CHOICES = [
        ('INTENSIVO', 'Intensivo'),
        ('S_INTENSIVO', 'Semi-Intensivo')
    ]

    date = models.DateField("Data")
    peso_medio_povoamento = models.FloatField("Peso Medio no Povoamento")
    peso_medio_despesca = models.FloatField("Peso Medio Esperado na Despeca")
    quant_peixe_povoamento = models.IntegerField("Quantidade de peixes no povoamento")
    idade_peixe = models.FloatField("Idade do peixe")
    type_system = models.CharField("Tipo de Sistema", max_length=12, choices=TYPE_SYSTEM_CHOICES)

class Despesca(models.Model):
    date = models.DateField("Data")
    peso_medio_final = models.FloatField("Peso Medio Final")
    quant_final = models.IntegerField("Quantidade Final de peixes")

class Ciclo(models.Model):
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    population = models.ForeignKey(Population, on_delete=models.CASCADE)
    despesca = models.ForeignKey(Despesca, on_delete=models.CASCADE)

class Biometria(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    date = models.DateField("Data")
    peso_medio = models.FloatField("Peso Medio")
    mortalidade = models.IntegerField("Mortalidade")