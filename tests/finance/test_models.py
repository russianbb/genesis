import pytest
from django.db import models
from finance.models import CostCenter, Receivable, ServiceOrder
from model_utils.choices import Choices
from utils.models import AbstractBaseModel


class TestServiceOrderModel:
    @classmethod
    def setup_class(cls):
        cls.model = ServiceOrder

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True

    def test_meta(self):
        assert self.model._meta.ordering == ["-created_at"]
        assert self.model._meta.verbose_name == "Ordem de Serviço"
        assert self.model._meta.verbose_name_plural == "Ordens de Serviço"

    def test_field_description(self):
        field = self.model._meta.get_field("description")

        assert field.max_length == 200
        assert field.unique is True
        assert field.verbose_name == "Descrição"
        assert type(field) == models.CharField

    def test_field_buy_order(self):
        field = self.model._meta.get_field("buy_order")

        assert field.max_length == 200
        assert field.blank is True
        assert field.verbose_name == "Ordem de Compra"
        assert type(field) == models.CharField

    def test_field_requester(self):
        field = self.model._meta.get_field("requester")

        assert field.max_length == 200
        assert field.blank is True
        assert field.verbose_name == "Solicitante"
        assert type(field) == models.CharField

    def test_str(self):
        instance = ServiceOrder(description="foo")
        assert str(instance) == "foo"


@pytest.mark.django_db
class TestCostCenterModel:
    @classmethod
    def setup_class(cls):
        cls.model = CostCenter

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True

    def test_meta(self):
        assert self.model._meta.ordering == ["-created_at"]
        assert self.model._meta.verbose_name == "Centro de Custo"
        assert self.model._meta.verbose_name_plural == "Centros de Custos"

    def test_field_description(self):
        field = self.model._meta.get_field("description")

        assert field.max_length == 200
        assert field.unique is True
        assert field.verbose_name == "Descrição"
        assert type(field) == models.CharField

    def test_str(self):
        instance = CostCenter(description="foo")
        assert str(instance) == "foo"

    def test_get_billings_amount(
        self, cost_center, invoice_received, invoice_not_received
    ):
        assert float(cost_center.get_billings_amount) == 33.33

    def test_get_billings_amount_null(self, cost_center):
        assert cost_center.get_billings_amount == "-"

    def test_get_billings_not_received(self, cost_center, invoice_not_received):
        assert float(cost_center.get_billings_not_received) == 11.11

    def test_get_billings_not_received_null(self, cost_center):
        assert cost_center.get_billings_not_received == "-"

    def test_get_billings_received(self, cost_center, invoice_received):
        assert float(cost_center.get_billings_received) == 22.22

    def test_get_billings_received_null(self, cost_center):
        assert cost_center.get_billings_received == "-"


@pytest.mark.django_db
class TestReceivableModel:
    @classmethod
    def setup_class(cls):
        cls.model = Receivable

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True

    def test_meta(self):
        assert self.model._meta.ordering == ["-issued_at", "-number"]
        assert self.model._meta.verbose_name == "Recebível"
        assert self.model._meta.verbose_name_plural == "Recebíveis"

    def test_upload_path(self):
        assert self.model.UPLOAD_PATH == "finance/receivables/"

    def test_field_number(self):
        field = self.model._meta.get_field("number")

        assert field.verbose_name == "Número"
        assert type(field) == models.PositiveIntegerField

    def test_field_issued_at(self):
        field = self.model._meta.get_field("issued_at")

        assert field.verbose_name == "Data de Emissão"
        assert type(field) == models.DateField

    def test_field_amount(self):
        field = self.model._meta.get_field("amount")

        assert field.max_digits == 10
        assert field.decimal_places == 2
        assert field.verbose_name == "Valor"
        assert type(field) == models.DecimalField

    def test_field_taxes(self):
        field = self.model._meta.get_field("taxes")

        assert field.max_digits == 10
        assert field.decimal_places == 2
        assert field.verbose_name == "Imposto"
        assert field.blank is True
        assert field.null is True
        assert type(field) == models.DecimalField

    def test_field_category(self):
        field = self.model._meta.get_field("category")
        RECEIVABLE_CATEGORY = Choices(
            ("invoice", "Nota Fiscal"),
            ("debit", "Nota de Débito"),
            ("loan", "Empréstimo"),
        )

        assert field.max_length == 20
        assert field.blank is False
        assert field.null is False
        assert field.verbose_name == "Categoria"
        assert field.choices == RECEIVABLE_CATEGORY
        assert type(field) == models.CharField

    def test_field_service_order(self):
        field = self.model._meta.get_field("service_order")

        assert field.related_model == ServiceOrder
        assert field.remote_field.related_name == "receivables"
        assert field.remote_field.on_delete.__name__ == "CASCADE"
        assert field.verbose_name == "Ordem de Serviço"
        assert type(field) == models.ForeignKey

    def test_field_cost_center(self):
        field = self.model._meta.get_field("cost_center")

        assert field.related_model == CostCenter
        assert field.remote_field.related_name == "receivables"
        assert field.remote_field.on_delete.__name__ == "CASCADE"
        assert field.verbose_name == "Centro de Custo"
        assert type(field) == models.ForeignKey

    def test_field_file(self):
        field = self.model._meta.get_field("file")

        assert field.upload_to.__name__ == "get_upload_to"
        assert field.blank is True
        assert field.verbose_name == "Arquivo"
        assert type(field) == models.FileField

    def test_field_is_received(self):
        field = self.model._meta.get_field("is_received")

        assert field.default is False
        assert field.verbose_name == "Já recebido?"
        assert type(field) == models.BooleanField

    def test_str(self, invoice_received):
        assert str(invoice_received) == "Nota Fiscal 002"

    def test_get_number_display(self, invoice_received):
        assert invoice_received.get_number_display == "002"

    def test_get_amount_display(self, invoice_received):
        assert invoice_received.get_amount_display == "22,22"

    def test_get_upload_filename(self, invoice_received):
        assert (
            invoice_received.get_upload_filename == "Nota Fiscal 002-Some Cost Center"
        )  # noqa

    def test_get_transaction_category(self, invoice_received, debit_received):
        assert invoice_received.get_transaction_category == "Nota Fiscal"
        assert debit_received.get_transaction_category == "Nota de Débito"

    def test_set_as_received(self, invoice_not_received):
        invoice_not_received.set_as_received
        assert invoice_not_received.is_received is True
