from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Sum
from model_utils.choices import Choices
from utils.constants import TRANSACTION_CATEGORY_ND, TRANSACTION_CATEGORY_NF
from utils.models import AbstractBaseModel

from .managers import BillManager, ExpenseManager, RevenueManager


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
        query = self.receivables.all().aggregate(Sum("amount"))
        if query.get("amount__sum"):
            return query["amount__sum"]
        return "-"

    @property
    def get_billings_not_received(self):
        query = (
            self.receivables.filter(is_received=False).all().aggregate(Sum("amount"))
        )
        if query.get("amount__sum"):
            return query["amount__sum"]
        return "-"

    @property
    def get_billings_received(self):
        query = self.receivables.filter(is_received=True).all().aggregate(Sum("amount"))
        if query.get("amount__sum"):
            return query["amount__sum"]
        return "-"


class Receivable(AbstractBaseModel):
    UPLOAD_PATH = "finance/receivables/"

    RECEIVABLE_CATEGORY = Choices(
        ("invoice", "Nota Fiscal"), ("debit", "Nota de Débito"), ("loan", "Empréstimo")
    )
    number = models.PositiveIntegerField(verbose_name="Número")
    issued_at = models.DateField(verbose_name="Data de Emissão")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    taxes = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Imposto", blank=True, null=True
    )
    category = models.CharField(
        choices=RECEIVABLE_CATEGORY,
        max_length=20,
        null=False,
        blank=False,
        verbose_name="Categoria",
    )
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        verbose_name="Ordem de Serviço",
        related_name="receivables",
    )
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.CASCADE,
        verbose_name="Centro de Custo",
        related_name="receivables",
    )
    file = models.FileField(upload_to=get_upload_to, verbose_name="Arquivo", blank=True)
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
            return TRANSACTION_CATEGORY_NF["description"]
        if self.category == "debit":
            return TRANSACTION_CATEGORY_ND["description"]

    @property
    def set_as_received(self):
        if not self.is_received:
            self.is_received = True
            self.save()


class TransactionCategory(AbstractBaseModel):
    CASH_FLOW_CHOICES = Choices(("revenue", "Receita"), ("expense", "Despesa"))
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
    UPLOAD_PATH = "finance/"

    due_date = models.DateField(
        verbose_name="Data de Vencimento", null=True, blank=True
    )
    transacted_at = models.DateField(
        verbose_name="Data da Transação", null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    cost_center = models.ForeignKey(
        CostCenter,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="Centro de Custo",
    )
    category = models.ForeignKey(
        TransactionCategory,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="Categoria",
    )
    notes = models.CharField(max_length=254, verbose_name="Anotações", blank=True)
    file = models.FileField(
        upload_to=get_upload_to, verbose_name="Comprovante", blank=True
    )
    bill = models.FileField(upload_to=get_upload_to, verbose_name="Boleto", blank=True)
    is_paid = models.BooleanField(verbose_name="Pago?", default=False)
    is_recurrent = models.BooleanField(verbose_name="Recorrente?", default=False)

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
        if not self.is_paid and self.due_date:
            subpath = f"bills/{self.due_date.strftime('%Y/%m')}"
            when = self.due_date.strftime("%d_%m_%Y")
        else:
            subpath = f"transactions/{self.transacted_at.strftime('%Y/%m')}"
            when = self.transacted_at.strftime("%d_%m_%Y")

        return f"{subpath}/{when}-{self.category}-{self.notes}-RS_{self.get_amount_display}"  # noqa

    @property
    def set_as_paid(self):
        if not self.is_paid:
            self.is_paid = True
            self.save()

    @property
    def create_recurrent(self):
        due_date = self.transacted_at + relativedelta(months=1)
        if self.due_date:
            due_date = self.due_date + relativedelta(months=1)

        recurrent = Transaction(
            amount=self.amount,
            cost_center=self.cost_center,
            category=self.category,
            notes=self.notes,
            due_date=due_date,
        )
        recurrent.save()


class Bill(Transaction):
    class Meta:
        proxy = True
        ordering = ["due_date", "id"]
        verbose_name = "Transação a Pagar"
        verbose_name_plural = "Transações a Pagar"

    objects = BillManager()


class Expense(Transaction):
    class Meta:
        proxy = True
        verbose_name = "Transação Paga"
        verbose_name_plural = "Transações Pagas"

    objects = ExpenseManager()


class Revenue(Transaction):
    class Meta:
        proxy = True
        verbose_name = "Transação Recebida"
        verbose_name_plural = "Transações Recebidas"

    objects = RevenueManager()
