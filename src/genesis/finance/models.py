from django.db import models
from model_utils.choices import Choices
from utils.models import AbstractBaseModel


class ServiceOrder(AbstractBaseModel):
    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )
    buy_order = models.CharField(max_length=200, verbose_name="Ordem de Compra")

    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"


class CostCenter(AbstractBaseModel):
    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )

    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custos"


class Category(AbstractBaseModel):
    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )

    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Transaction(AbstractBaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    CASH_FLOW_CHOICES = Choices(("receipt", "Receita"), ("expense", "Despesa"))
    cash_flow = models.CharField(
        choices=CASH_FLOW_CHOICES,
        max_length=15,
        null=False,
        blank=False,
        verbose_name="Fluxo",
        default="expense",
    )
    category = models.ForeignKey(
        Category,
        related_name="transaction",
        on_delete=models.CASCADE,
        verbose_name="Cetegoria",
    )
    cost_center = models.ForeignKey(
        CostCenter,
        related_name="transaction",
        on_delete=models.CASCADE,
        verbose_name="Centro de Custo",
    )
    notes = models.CharField(max_length=254, verbose_name="Anotações")
    receipt = models.FileField(
        upload_to="finance/receipts/", verbose_name="Comprovante"
    )
    transacted_at = models.DateField(verbose_name="Data da Transação")

    def __str__(self):
        return (
            f"<CashFlow: {self.cash_flow} - CostCenter: {self.cost_center}"
            "- Category: {self.category} - Amount: {self.amount}>"
        )

    class Meta:
        ordering = ["transacted_at", "id"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
