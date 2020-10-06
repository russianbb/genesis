from django.db import models
from comercial.models import Company
from utils.models import AbstractBaseModel

class OnixProduct(AbstractBaseModel):
    UNIT_MESURE_CHOICES = (
        ('KG', 'Kilos'),
        ('G', 'Gramas'),
        ('L', 'Litros'),
        ('ML', 'Mililitros'),
        ('CX', 'Caixa')
    )
    description = models.CharField(verbose_name='Descrição completa', max_length=200, help_text='Normalmente segue o padrão: Nome do Produto - Tamanho da Embalagem Tipo de Unidade.')
    prefix = models.CharField(verbose_name='Nome do produto', max_length=150, help_text='Apenas o nome, sem complementos. Exemplo: Cruiser, Cruiser Opti, Zapp QI, Zapp Pro.')
    unit_size = models.CharField(verbose_name='Tamanho da embalagem', max_length=4, help_text='Tamanho da unidade vendida. Se for vendido em caixa, utilize " 1 ".')
    unit_mesure = models.CharField(verbose_name='Tipo de unidade', max_length=2, choices=UNIT_MESURE_CHOICES, help_text='Unidade em que o produto é vendido ou medido no estoque')
    unit_volume = models.DecimalField(verbose_name='Volume', max_digits=7, decimal_places=3, help_text='Volume da unidade vendida. Difere da embalagem em casos de caixas, frascos, pacotes, etc')

    class Meta:
        ordering = ['prefix', 'unit_volume']
        verbose_name = 'Produto Onix'
        verbose_name_plural = 'Produtos Onix'
        unique_together = [["prefix", "unit_size", "unit_mesure", "unit_volume"]]

    def __str__(self):
        return f'{self.description} [{self.pk}]'


class SyngentaProduct(AbstractBaseModel):
    product_onix = models.ForeignKey(OnixProduct, on_delete=models.CASCADE, verbose_name='Produto Onix')
    agicode = models.CharField(verbose_name='Agicode',max_length=20, primary_key=True)
    family = models.CharField(verbose_name='Família', max_length=150)
    description = models.CharField(verbose_name='Descrição completa', max_length=200)

    class Meta:
        ordering = ['description']
        verbose_name = 'Produto Syngenta'
        verbose_name_plural = 'Produtos Syngenta'
        unique_together = [["product_onix", "agicode"]]

    def __str__(self):
        return f'{self.description} [{self.agicode}]'

    def get_onix_product(self):
        return f'{self.product_onix}'


class CompanyProduct(AbstractBaseModel):
    product_onix = models.ForeignKey(OnixProduct, on_delete=models.CASCADE, verbose_name='Produto Onix')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Distribuidor')
    code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Código', help_text='Código utilizado pelo distribuidor para identificar o produto nos relatórios.')
    description = models.CharField(max_length=80, null=True, blank=True, verbose_name='Descrição', help_text='Código utilizado pelo distribuidor para identificar o produto nos relatórios.')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Produto Distribuidor'
        verbose_name_plural = 'Produtos Distribuidor'
        unique_together = [["product_onix", "company", "code", "description"]]

    def __str__(self):
        return f'{self.company.trade_name} - {self.product_onix}'

    def get_onix_product(self):
        return f'{self.product_onix}'

    def get_syngenta_product(self):
        return f'{self.product_syngenta}'
