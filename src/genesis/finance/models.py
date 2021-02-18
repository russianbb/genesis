from django.db import models
from model_utils.choices import Choices
from utils.models import AbstractBaseModel


class ServiceOrder(AbstractBaseModel):
    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )
    buy_order = models.CharField(
        max_length=200, verbose_name="Ordem de Compra", blank=True
    )
    requester = models.CharField(max_length=200, verbose_name="Solicitante", blank=True)

    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"


class Invoice(AbstractBaseModel):
    INVOICE_CATEGORY = Choices(
        ("invoice", "Nota Fiscal"), ("debit", "Nota de Débito"), ("loan", "Empréstimo")
    )
    number = models.PositiveIntegerField(verbose_name="Número")
    issued_at = models.DateField(verbose_name="Data de Emissão")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    taxes = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Imposto", blank=True, null=True
    )
    category = models.CharField(
        choices=INVOICE_CATEGORY,
        max_length=20,
        null=False,
        blank=False,
        verbose_name="Categoria",
    )
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        verbose_name="Ordem de Serviço",
        related_name="invoices",
    )
    document = models.FileField(
        upload_to="finance/invoices/", verbose_name="DANFE", blank=True
    )

    def __str__(self):
        return f"{self.get_category_display()} {self.number}"

    class Meta:
        ordering = ["issued_at", "number"]
        verbose_name = "Recebível"
        verbose_name_plural = "Recebíveis"


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
    CASH_FLOW_CHOICES = Choices(("receipt", "Receita"), ("expense", "Despesa"))
    cash_flow = models.CharField(
        choices=CASH_FLOW_CHOICES,
        max_length=15,
        null=False,
        blank=False,
        verbose_name="Fluxo",
        default="expense",
    )
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
    transacted_at = models.DateField(verbose_name="Data da Transação")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    cost_center = models.ForeignKey(
        CostCenter,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="Centro de Custo",
    )
    category = models.ForeignKey(
        Category,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="Cetegoria",
    )
    notes = models.CharField(max_length=254, verbose_name="Anotações", blank=True)
    document = models.FileField(
        upload_to="finance/transactions/", verbose_name="Comprovante", blank=True
    )

    def __str__(self):
        return f"{self.cost_center} | {self.category} | {self.amount}"

    class Meta:
        ordering = ["transacted_at", "id"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
