from django.db import models
from django.conf import settings


class Casa(models.Model):
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="minhas_casas")
    titulo =models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=200)
    num_quartos =models.PositiveIntegerField(default=1)#tem no minimo um quarto
    preco_dia = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.dono}, sua casa foi registrada com sucesso."

class Aluguel(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name="alugueis_da_casa")
    hospede = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="casas_alugadas")
    data_entrada = models.DateField()
    data_saida = models.DateField() 
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2)
    datas_aluguel = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Alugueis'

    def __str__(self) -> str:
        return f"A casa {self.casa} foi aluguada para {self.hospede} no período de {self.data_entrada} até {self.data_saida}"