from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group)


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Cria e salva usuário a partir de e-mail e senha
        """
        if not email:
            raise ValueError('Usuário deve ter endereço de e-mail')

        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Cria e salva super usuário a partir de e-mail e senha
        """
        user = self.create_user(email, password=password)
        user.admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField('CPF', unique=True, max_length=11)
    email = models.EmailField('e-mail', unique=True)
    instituicao = models.CharField('instituição', max_length=255)
    curso = models.CharField('curso', max_length=255)
    ativo = models.BooleanField(default=True)
    admin = models.BooleanField('administrador', default=False)

    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ('nome_completo', 'cpf')

    @property
    def username(self):
        return self.get_short_name()

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    def __str__(self):
        if self.nome_completo:
            return self.nome_completo
        return self.get_short_name()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.nome_completo

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin
