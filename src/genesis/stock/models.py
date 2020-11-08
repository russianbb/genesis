from comercial.models import Company, Store
from django.db import models
from products.models import OnixProduct
from utils.models import AbstractBaseModel, AbstractStockModel


class CutDate(AbstractBaseModel):
    date = models.DateField(
        verbose_name="Data Base", help_text="Data de mensuração do estoque"
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Descrição",
        help_text="Nome do projeto ou descrição do momento em que se mensura os estoques",  # noqa: E501
    )

    class Meta:
        ordering = ("date",)
        verbose_name = "Data Base"
        verbose_name_plural = "Datas Base"
        unique_together = ("date", "description")

    def __str__(self):
        return self.date.strftime("%d/%m/%y")


class SyngentaBalance(models.Model):
    date = models.ForeignKey(
        to=CutDate, on_delete=models.CASCADE, verbose_name="Data Base",
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="Distribuidor",
    )
    product = models.ForeignKey(
        to=OnixProduct, on_delete=models.CASCADE, verbose_name="Produto Onix",
    )
    balance = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="Saldo Syngenta",
        help_text="Saldo de estoque informado pela Syngenta. (Posição Sales Force)",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("date", "company", "product")
        verbose_name = "Saldo Syngenta"
        verbose_name_plural = "Saldos Syngenta"
        unique_together = ("date", "company", "product", "balance")

    def __str__(self):
        return self.balance


class Justification(AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate, on_delete=models.CASCADE, verbose_name="Data Base",
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="Distribuidor",
    )
    product = models.ForeignKey(
        to=OnixProduct, on_delete=models.CASCADE, verbose_name="Produto Onix",
    )
    description = models.TextField(verbose_name="Justificativa")

    class Meta:
        ordering = ("date", "company", "product")
        verbose_name = "Justificativa"
        verbose_name_plural = "Justificativas"
        unique_together = ("date", "company", "product")

    def __str__(self):
        return self.description


class Item(AbstractStockModel, AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate, on_delete=models.CASCADE, verbose_name="Data Base",
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="Distribuidor",
    )
    product = models.ForeignKey(
        to=OnixProduct, on_delete=models.CASCADE, verbose_name="Produto Onix",
    )
    store = models.ForeignKey(
        to=Store, on_delete=models.CASCADE, verbose_name="Filial", related_name="item",
    )

    class Meta:
        ordering = ("date", "company", "product", "store")
        verbose_name = "Item"
        verbose_name_plural = "Itens"


class Index(AbstractStockModel, AbstractBaseModel):
    date = models.ForeignKey(
        to=CutDate, on_delete=models.CASCADE, verbose_name="Data Base",
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="Distribuidor",
    )
    product = models.ForeignKey(
        to=OnixProduct, on_delete=models.CASCADE, verbose_name="Produto Onix",
    )
    adjust = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name="Ajuste", null=True, blank=True,
    )
    syngenta_balance = models.ForeignKey(
        to=SyngentaBalance,
        on_delete=models.CASCADE,
        verbose_name="Saldo Syngenta",
        related_name="index",
    )
    difference = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="Divergência",
        null=True,
        blank=True,
    )
    justification = models.ForeignKey(
        to=Justification,
        on_delete=models.CASCADE,
        verbose_name="Justificativa",
        related_name="index",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("date", "company", "product")
        verbose_name = "Consolidado"
        verbose_name_plural = "Consolidados"
        unique_together = ("date", "company", "product")


class Document(AbstractBaseModel):
    CATEGORY_CHOICES = (
        ("import", "Modelo de Importação"),
        ("justification", "Modelo de Justificativas"),
    )
    date = models.ForeignKey(
        to=CutDate,
        on_delete=models.CASCADE,
        verbose_name="Data Base",
        related_name="document",
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name="Distribuidor",
        related_name="document",
    )
    category = models.CharField(
        verbose_name="Tipo de Documento", max_length=100, choices=CATEGORY_CHOICES,
    )
    file = models.FileField(verbose_name="Arquivo", upload_to="stock/")

    class Meta:
        ordering = ("date", "company", "category")
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        unique_together = ("date", "company", "category")

    def __str__(self):
        return f"{self.date.name} - {self.company.company_name}"
