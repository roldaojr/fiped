from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Usuário deve ter endereço de e-mail')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(PermissionsMixin, AbstractBaseUser):
    nome_completo = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=50,
                           blank=False, null=True,
                           verbose_name='CPF / Passaporte')
    email = models.EmailField('e-mail', unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True, verbose_name='ativo')
    date_joined = models.DateTimeField(default=timezone.now, editable=False,
                                       verbose_name='cadastro em')

    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    @property
    def username(self):
        return self.get_short_name()

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        if self.nome_completo:
            return self.nome_completo
        return self.get_short_name()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        if self.nome_social:
            return self.nome_social
        return self.nome_completo
