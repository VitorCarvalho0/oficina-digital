from django.db import models
from django.contrib.auth.models import User

class Atendimento(models.Model):
    STATUS_CHOICES = [
        ('recebido', 'Recebido'),
        ('andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Dados do Cliente
    cliente = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # Dados do Veículo
    veiculo = models.CharField(max_length=100)
    placa = models.CharField(max_length=20)
    letra_vidro = models.CharField(max_length=10, blank=True, null=True)
    ano = models.IntegerField()
    km = models.IntegerField()
    
    # Fotos dos Ângulos Padrão
    foto_frente = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    foto_tras = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    foto_lat_esq = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    foto_lat_dir = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    
    # Observações e Status
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido')
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.veiculo} ({self.placa})"


# Novo Model para salvar fotos extras dinâmicas ilimitadas
class FotoAtendimento(models.Model):
    atendimento = models.ForeignKey(Atendimento, related_name='fotos_extras', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default='Detalhe') # Ex: Roda Direita
    imagem = models.ImageField(upload_to='veiculos/extras/')

    def __str__(self):
        return f"{self.titulo} - {self.atendimento.placa}"
