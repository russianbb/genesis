from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from django.db import models
from finance.models import CostCenter, Transaction, TransactionCategory, get_upload_to
from utils.models import AbstractBaseModel

pytestmark = pytest.mark.django_db


class TestTransactionModel:
    @classmethod
    def setup_class(cls):
        cls.model = Transaction

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True

    def test_meta(self):
        assert self.model._meta.ordering == ["-transacted_at", "-id"]
        assert self.model._meta.verbose_name == "Transação"
        assert self.model._meta.verbose_name_plural == "Transações"

    def test_upload_path(self):
        assert self.model.UPLOAD_PATH == "finance/"

    def test_field_due_date(self):
        field = self.model._meta.get_field("due_date")

        assert field.verbose_name == "Data de Vencimento"
        assert type(field) == models.DateField
        assert field.null is True
        assert field.blank is True

    def test_field_transacted_at(self):
        field = self.model._meta.get_field("transacted_at")

        assert field.verbose_name == "Data da Transação"
        assert type(field) == models.DateField
        assert field.null is True
        assert field.blank is True

    def test_field_amount(self):
        field = self.model._meta.get_field("amount")

        assert field.max_digits == 10
        assert field.decimal_places == 2
        assert field.verbose_name == "Valor"
        assert type(field) == models.DecimalField

    def test_field_cost_center(self):
        field = self.model._meta.get_field("cost_center")

        assert field.related_model == CostCenter
        assert field.remote_field.related_name == "transactions"
        assert field.remote_field.on_delete.__name__ == "CASCADE"
        assert field.verbose_name == "Centro de Custo"
        assert type(field) == models.ForeignKey

    def test_field_category(self):
        field = self.model._meta.get_field("category")

        assert field.related_model == TransactionCategory
        assert field.remote_field.related_name == "transactions"
        assert field.remote_field.on_delete.__name__ == "CASCADE"
        assert field.verbose_name == "Categoria"
        assert type(field) == models.ForeignKey

    def test_field_notes(self):
        field = self.model._meta.get_field("notes")

        assert field.max_length == 254
        assert field.verbose_name == "Anotações"
        assert field.blank is True

    def test_field_file(self):
        field = self.model._meta.get_field("file")

        assert field.upload_to.__name__ == "get_upload_to"
        assert field.blank is True
        assert field.verbose_name == "Comprovante"
        assert type(field) == models.FileField

    def test_field_bill(self):
        field = self.model._meta.get_field("bill")

        assert field.upload_to.__name__ == "get_upload_to"
        assert field.blank is True
        assert field.verbose_name == "Boleto"
        assert type(field) == models.FileField

    def test_field_is_paid(self):
        field = self.model._meta.get_field("is_paid")

        assert field.default is False
        assert field.verbose_name == "Pago?"
        assert type(field) == models.BooleanField

    def test_field_is_recurrent(self):
        field = self.model._meta.get_field("is_recurrent")

        assert field.default is False
        assert field.verbose_name == "Recorrente?"
        assert type(field) == models.BooleanField


def test_str_with_notes(transaction_paid):
    assert str(transaction_paid) == "Some Notes"


def test_str_without_notes(transaction):
    assert str(transaction) == "Some Category"


def test_get_amount_display(transaction):
    assert transaction.get_amount_display == "1,99"


def test_get_upload_filename_not_paid_due_date(transaction_not_paid):
    filename = "bills/2021/01/01_01_2021-Some Category--RS_1,99"
    assert transaction_not_paid.get_upload_filename == filename


def test_bill_get_upload_filename_paid(transaction_paid):
    filename = "transactions/2021/01/01_01_2021-Some Category-Some Notes-RS_1,99"
    assert transaction_paid.get_upload_filename == filename


def test_set_as_paid(transaction_not_paid):
    transaction_not_paid.set_as_paid
    assert transaction_not_paid.is_paid is True


@patch("finance.models.Transaction")
def test_create_recurrent_with_due_date(mock_model, transaction_paid_with_due_date):
    new_due_date = date(2021, 2, 1)

    transaction_paid_with_due_date.create_recurrent

    mock_model.assert_called_once_with(
        amount=transaction_paid_with_due_date.amount,
        cost_center=transaction_paid_with_due_date.cost_center,
        category=transaction_paid_with_due_date.category,
        notes=transaction_paid_with_due_date.notes,
        due_date=new_due_date,
    )

    mock_model.return_value.save.assert_called_once()


@patch("finance.models.Transaction")
def test_create_recurrent_without_due_date(mock_model, transaction_paid):
    new_due_date = date(2021, 2, 1)

    transaction_paid.create_recurrent

    mock_model.assert_called_once_with(
        amount=transaction_paid.amount,
        cost_center=transaction_paid.cost_center,
        category=transaction_paid.category,
        notes=transaction_paid.notes,
        due_date=new_due_date,
    )

    mock_model.return_value.save.assert_called_once()


def test_get_upload_to():
    instance = MagicMock(UPLOAD_PATH="foo", get_upload_filename="bar")
    response = get_upload_to(instance, "file.ext")
    assert response == "foo/bar.ext"
