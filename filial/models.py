from django.db import models


class Filial(models.Model):

    class Meta:
        verbose_name = 'Filiais'

    nome = models.CharField(max_length=100)
    matriz = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}'
