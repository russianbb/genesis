from django.db import models
from utils.models import AbstractBaseModel
from comercial.models import Company, Store
from products.models import OnixProduct

class CutDate(AbstractBaseModel):
    date = models.DateField(
        verbose_name='Data Base',
        help_text='Data de mensuração do estoque'
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Descrição',
        help_text='Nome do projeto ou descrição do momento em que se mensura os estoques'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Data Base'
        verbose_name_plural = 'Datas Base'
        unique_together = ('date', 'description')

    def __str__(self):
        return self.date.strftime("%d/%m/%y")


class SyngentaBalance(models.Model):
    date = models.ForeignKey(
        to=CutDate,
        on_delete=models.CASCADE,
        verbose_name='Data Base',
        related_name='syngenta_balance',
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name='Distribuidor',
        related_name='syngenta_balance',
    )
    product = models.ForeignKey(
        to=OnixProduct,
        on_delete=models.CASCADE,
        verbose_name='Produto Onix',
        related_name='syngenta_balance',
    )
    balance = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Saldo Syngenta',
        help_text='Saldo de estoque informado pela Syngenta. (Posição Sales Force)',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('date', 'company', 'product')
        verbose_name = 'Saldo Syngenta'
        verbose_name_plural = 'Saldos Syngenta'
        unique_together = ('date', 'company', 'product', 'balance')

class Justification(AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate,
        on_delete=models.CASCADE,
        verbose_name='Data Base',
        related_name='justification',
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name='Distribuidor',
        related_name='justification',
    )
    product = models.ForeignKey(
        to=OnixProduct,
        on_delete=models.CASCADE,
        verbose_name='Produto Onix',
        related_name='justification',
    )
    description = models.TextField(
        verbose_name='Justificativa'
    )

    class Meta:
        ordering = ('date', 'company', 'product')
        verbose_name = 'Justificativa'
        verbose_name_plural = 'Justificativas'
        unique_together = ('date', 'company', 'product')

class Item(AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate,
        on_delete=models.CASCADE,
        verbose_name='Data Base',
        related_name='item',
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name='Distribuidor',
        related_name='item',
    )
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        verbose_name='Filial',
        related_name='item',
    )
    product = models.ForeignKey(
        to=OnixProduct,
        on_delete=models.CASCADE,
        verbose_name='Produto Onix',
        related_name='item',
    )
    owned = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='EF',
        help_text='Saldo de estoque físico',
        null=True,
        blank=True,
    )
    sold = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='VEF',
        help_text='Saldo de venda para entrega futura faturada com CFOP 5922, 6922',
        null=True,
        blank=True,
    )
    sent = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Em Terceiros',
        help_text='Saldo de estoque físico do distribuidor armazenado em poder de terceiros (Remessa para enviada)',
        null=True,
        blank=True,
    )
    received = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='De Terceiros',
        help_text='Saldo de estoque físico de terceiros armazenado em poder do distribuidor (Remessa recebida)',
        null=True,
        blank=True,
    )
    transit = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Em Trânsito',
        help_text='Saldo de estoque físico em trânsito',
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Saldo Calculado',
        help_text='Saldo de estoque calculado. Saldo = EF - VEF + Em Terceiros - De Terceiros +- Transito',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('date', 'company', 'product', 'store')
        verbose_name = 'Item Base'
        verbose_name_plural = 'Itens Base'

class Index(AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate,
        on_delete=models.CASCADE,
        verbose_name='Data Base',
        related_name='index',
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name='Distribuidor',
        related_name='index',
    )
    product = models.ForeignKey(
        to=OnixProduct,
        on_delete=models.CASCADE,
        verbose_name='Produto Onix',
        related_name='index',
    )
    owned = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='EF',
        help_text='Saldo de estoque físico',
        null=True,
        blank=True,
    )
    sold = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='VEF',
        help_text='Saldo de venda para entrega futura faturada com CFOP 5922, 6922',
        null=True,
        blank=True,
    )
    sent = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Em Terceiros',
        help_text='Saldo de estoque físico do distribuidor armazenado em poder de terceiros (Remessa para enviada)',
        null=True,
        blank=True,
    )
    received = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='De Terceiros',
        help_text='Saldo de estoque físico de terceiros armazenado em poder do distribuidor (Remessa recebida)',
        null=True,
        blank=True,
    )
    transit = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Em Trânsito',
        help_text='Saldo de estoque físico em trânsito',
        null=True,
        blank=True,
    )
    adjust = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Ajuste',
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name='Saldo Calculado',
        help_text='Saldo de estoque calculado. Saldo = EF - VEF + Em Terceiros - De Terceiros +- Transito +- Ajuste',
        null=True,
        blank=True,
    )
    syngenta_balance = models.ForeignKey(
        to=SyngentaBalance,
        on_delete=models.CASCADE,
        verbose_name='Saldo Syngenta',
        related_name='index',
    )
    justification = models.ForeignKey(
        to=Justification,
        on_delete=models.CASCADE,
        verbose_name='Justificativa',
        related_name='index',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('date', 'company', 'product')
        verbose_name = 'Consolidado'
        verbose_name_plural = 'Consolidados'
        unique_together = ('date', 'company', 'product')


