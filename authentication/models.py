from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, GroupManager
from django.contrib.auth.models import AbstractUser
from filial.models import Filial


class FuncaoManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Funcao(models.Model):
    class Meta:
        verbose_name_plural = "Funções"

    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
        related_name='permissions_set',
        related_query_name='permissions'
    )

    objects = GroupManager()

    def __str__(self) -> str:
        return f'{self.name}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=False)
    cpf = models.CharField(unique=True, null=True, blank=True, max_length=15)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    data_admissao = models.DateField(
        verbose_name='Data de admissão', default=timezone.now)
    data_senha = models.DateField(
        verbose_name='Data da ultima troca de senha',
        default=timezone.now)
    filial = models.ForeignKey(Filial, on_delete=models.DO_NOTHING, blank=True, null=True)
    funcoes = models.ManyToManyField(
        Funcao,
        verbose_name=_("funcoes"),
        blank=True,
    )

    groups = None
