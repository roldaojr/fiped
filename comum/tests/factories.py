from django.contrib.auth.models import Permission
from random import randrange
import factory
from faker.providers import BaseProvider
from ..models import Usuario


class CpfProvider(BaseProvider):
    def cpf(self):
        def digito_cpf(cpf):
            res = []
            for i, a in enumerate(cpf):
                b = len(cpf) + 1 - i
                res.append(b * a)
            res = sum(res) % 11

            if res > 1:
                return 11 - res
            else:
                return 0

        cpf = [randrange(10) for x in range(9)]
        cpf += [digito_cpf(cpf)]
        cpf += [digito_cpf(cpf)]

        cpfVal = 0
        for i, v in enumerate(cpf):
            cpfVal += v * (10 ** (len(cpf) - 1 - i))
        return cpfVal


factory.Faker.add_provider(CpfProvider, locale='pt_BR')


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    nome_completo = factory.Faker('name')
    email = factory.Faker('email')
    cpf = factory.Faker('cpf', locale='pt_BR')
    is_active = True

    @factory.post_generation
    def perms(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for perm in extracted:
                app_label, codename = perm.split('.')
                permission = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename)
                self.user_permissions.add(permission)
