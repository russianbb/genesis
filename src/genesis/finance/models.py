from decimal import Decimal

from django.db import models
from django.db.models import Sum
from model_utils.choices import Choices
from utils.constants import CATEGORY_ND, CATEGORY_NF
from utils.models import AbstractBaseModel


def get_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return f"{instance.UPLOAD_PATH}/{instance.get_upload_filename}.{ext}"


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
        ordering = ["-created_at"]
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"


class CostCenter(AbstractBaseModel):
    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )

    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custos"

    @property
    def get_billings_amount(self):
        query = self.invoices.all().aggregate(Sum("amount"))
        if query.get("amount__sum"):
            return query["amount__sum"]
        return 0

    @property
    def get_billings_not_received(self):
        query = self.invoices.filter(is_received=False).all().aggregate(Sum("amount"))
        if query.get("amount__sum"):
            return query["amount__sum"]
        return 0


class Invoice(AbstractBaseModel):
    UPLOAD_PATH = "finance/invoices/"

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
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.CASCADE,
        verbose_name="Centro de Custo",
        related_name="invoices",
    )
    document = models.FileField(
        upload_to=get_upload_to, verbose_name="Arquivo", blank=True
    )
    is_received = models.BooleanField(verbose_name="Já recebido?", default=False)

    class Meta:
        ordering = ["-issued_at", "-number"]
        verbose_name = "Recebível"
        verbose_name_plural = "Recebíveis"

    def __str__(self):
        return f"{self.get_category_display()} {self.number:03d}"

    @property
    def get_number_display(self):
        return f"{self.number:03d}"

    @property
    def get_amount_display(self):
        return (
            f"{Decimal('%0.2f' % self.amount):,}".replace(",", "d")
            .replace(".", ",")
            .replace("d", ".")
        )

    @property
    def get_upload_filename(self):
        return f"{self}-{self.cost_center}"

    @property
    def get_transaction_category(self):
        if self.category == "invoice":
            return CATEGORY_NF["description"]
        if self.category == "debit":
            return CATEGORY_ND["description"]
        return None

    @property
    def set_received(self):
        if not self.is_received:
            self.is_received = True
            self.save()


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
        ordering = ["description"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Transaction(AbstractBaseModel):
    UPLOAD_PATH = "finance/transactions/"

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
        verbose_name="Categoria",
    )
    notes = models.CharField(max_length=254, verbose_name="Anotações", blank=True)
    document = models.FileField(
        upload_to=get_upload_to, verbose_name="Comprovante", blank=True
    )

    class Meta:
        ordering = ["-transacted_at", "-id"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        if not self.notes:
            return self.category.description
        return self.notes

    @property
    def get_amount_display(self):
        return (
            f"{Decimal('%0.2f' % self.amount):,}".replace(",", "d")
            .replace(".", ",")
            .replace("d", ".")
        )

    @property
    def get_upload_filename(self):
        subpath = self.transacted_at.strftime("%Y/%m/")
        when = self.transacted_at.strftime("%d_%m_%Y")
        return f"{subpath}/{when}-{self.category}-{self.notes}-RS_{self.get_amount_display}"  # noqa
