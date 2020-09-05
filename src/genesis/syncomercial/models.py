from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here

class Distribuidor(models.Model):
    code_sap = models.CharField(max_length = 8, unique=True)
    company_name = models.CharField(max_length = 100)
    nome_fantasia = models.CharField(max_length = 50)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    historico = HistoricalRecords()

    def __str__(self):
        return self.razao_social

    def fantasia(self):
        return self.nome_fantasia
    
    class Meta:
        ordering = ['razao_social']
        verbose_name = 'Distribuidor'
        verbose_name_plural = '1.0 - Cadastro de Distribuidores'


class Filial(models.Model):
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE)
    codigo = models.CharField(max_length = 15, null=True, blank=True)
    nome = models.CharField(max_length = 50, null=True, blank=True)
    cnpj = models.CharField(max_length = 14)
    responsavel = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ddd = models.CharField(max_length = 2, null=True, blank=True)
    telefone = models.CharField(max_length = 9, null=True, blank=True)
    endereco = models.CharField(max_length = 250)
    cidade = models.CharField(max_length = 50)
    estado = models.CharField(max_length = 2)
    codibge = models.CharField(max_length = 9, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    controla_estoque = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    historico = HistoricalRecords()

    def __str__(self):
        if self.nome:
            return f"{self.distribuidor.razao_social} - {self.nome}"
        else: 
            return f"{self.distribuidor.razao_social} - {self.cidade}"

    class Meta():
        ordering = ['distribuidor__razao_social', 'cidade', 'nome']
        verbose_name = 'Filial'
        verbose_name_plural = '1.1 - Cadastro de Filiais'
        unique_together = [['cnpj', 'codigo', 'nome', 'distribuidor_id']]


class Responsavel(models.Model):
    atuacao = (('Crop', 'Crop'),('Seeds','Seeds'), ('Ambos','Ambos'))
    nome = models.CharField(max_length = 50)
    cargo = models.CharField(max_length = 30, null=True, blank=True)
    atuacao = models.CharField(max_length = 5, choices=atuacao)
    email = models.EmailField(null=True, blank=True)
    ddd1 = models.CharField(max_length = 2, null=True, blank=True)
    telefone1 = models.CharField(max_length = 9, null=True, blank=True)
    ramal1 = models.CharField(max_length = 4, null=True, blank=True)
    ddd2 = models.CharField(max_length = 2, null=True, blank=True)
    telefone2 = models.CharField(max_length = 9, null=True, blank=True)
    ramal2 = models.CharField(max_length = 4, null=True, blank=True)
    anotacao = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    historico = HistoricalRecords()

    def __str__(self):
        if self.ddd1 and self.telefone1:
            return f"{self.nome} - ({self.ddd1}) {self.telefone1[-9:-4]}-{self.telefone1[-4:]}"
        else:
            return self.nome

    class Meta():
        ordering = ['nome']
        verbose_name = 'Responsável'
        verbose_name_plural = '3.0 - Cadastro de Responsáveis'

    @property
    def contato1(self):
        if self.ddd1 and self.telefone1:
            return f'({self.ddd1}) {self.telefone1[-9:-4]}-{self.telefone1[-4:]}'

    @property
    def contato2(self):
        if self.ddd2 and self.telefone2:
            return f'({self.ddd2}) {self.telefone2[-9:-4]}-{self.telefone2[-4:]}'


class Responsavel_Distribuidor(models.Model):
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    historico = HistoricalRecords()

    class Meta:
        ordering = ['distribuidor__razao_social', 'responsavel__nome']
        unique_together = ('distribuidor', 'responsavel')
        verbose_name = 'Responsável pelo Distribuidor'
        verbose_name_plural = '9.2 - Responsável pelo Distribuidor'


class RTV(models.Model):
    nome = models.CharField(max_length = 50)
    code_spoca = models.CharField(max_length = 8, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ddd1 = models.CharField(max_length=2, null=True, blank=True)
    telefone1 = models.CharField(max_length=9, null=True, blank=True)
    ramal1 = models.CharField(max_length=4, null=True, blank=True)
    ddd2 = models.CharField(max_length=2, null=True, blank=True)
    telefone2 = models.CharField(max_length=9, null=True, blank=True)
    ramal2 = models.CharField(max_length=4, null=True, blank=True)
    anotacao = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    historico = HistoricalRecords()

    def __str__(self):
        if self.ddd1 and self.telefone1:
            return f"{self.nome} - ({self.ddd1}) {self.telefone1[-9:-4]}-{self.telefone1[-4:]}"
        else:
            return self.nome

    @property
    def contato1(self):
        if self.ddd1 and self.telefone1:
            return f'({self.ddd1}) {self.telefone1[-9:-4]}-{self.telefone1[-4:]}'

    @property
    def contato2(self):
        if self.ddd2 and self.telefone2:
            return f'({self.ddd2}) {self.telefone2[-9:-4]}-{self.telefone2[-4:]}'

    class Meta():
        ordering = ['nome']
        verbose_name = 'RTV'
        verbose_name_plural = '2.0 - Cadastro de RTVs'


class RTV_Distribuidor(models.Model):
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE)
    RTV = models.ForeignKey(RTV, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    historico = HistoricalRecords()

    class Meta:
        ordering = ['distribuidor__razao_social', 'RTV__nome']
        unique_together = ('distribuidor', 'RTV')
        verbose_name = 'RTV do Distribuidor'
        verbose_name_plural = '9.1 - RTV do Distribuidor'