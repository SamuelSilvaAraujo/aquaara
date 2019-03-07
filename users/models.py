from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, cpf, name, password=None):
        if not cpf:
            raise ValueError('CPF é Obrigatório')

        user = self.model(
            cpf=cpf,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, name, password):
        user = self.create_user(
            cpf,
            password=password,
            name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    cpf = models.CharField("CPF", unique=True, max_length=11)
    name = models.CharField("Nome", max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.cpf

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin