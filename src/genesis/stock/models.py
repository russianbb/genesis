from comercial.models import Company, Store
from django.db import models
from products.models import OnixProduct
from projects.models import Project
from utils.models import AbstractBaseModel, AbstractStockModel


class SyngentaBalance(models.Model):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, verbose_name="Projeto",
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
        ordering = ("project", "company", "product")
        verbose_name = "Saldo Syngenta"
        verbose_name_plural = "Saldos Syngenta"
        unique_together = ("project", "company", "product", "balance")

    def __str__(self):
        return self.balance


class Justification(AbstractBaseModel):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, verbose_name="Projeto",
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="Distribuidor",
    )
    product = models.ForeignKey(
        to=OnixProduct, on_delete=models.CASCADE, verbose_name="Produto Onix",
    )
    description = models.TextField(verbose_name="Justificativa")

    class Meta:
        ordering = ("project", "company", "product")
        verbose_name = "Justificativa"
        verbose_name_plural = "Justificativas"
        unique_together = ("project", "company", "product")

    def __str__(self):
        return self.description


class Item(AbstractStockModel, AbstractBaseModel):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, verbose_name="Project",
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
        ordering = ("project", "company", "product", "store")
        verbose_name = "Item"
        verbose_name_plural = "Itens"


class Index(AbstractStockModel, AbstractBaseModel):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, verbose_name="Projeto",
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
        ordering = ("project", "company", "product")
        verbose_name = "Consolidado"
        verbose_name_plural = "Consolidados"
        unique_together = ("project", "company", "product")
