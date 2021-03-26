import pytest
from django.db import models
from finance.models import TransactionCategory
from model_utils.choices import Choices
from utils.models import AbstractBaseModel

pytestmark = pytest.mark.django_db


class TestTransactionCategoryModel:
    @classmethod
    def setup_class(cls):
        cls.model = TransactionCategory

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True

    def test_meta(self):
        assert self.model._meta.ordering == ["description"]
        assert self.model._meta.verbose_name == "Categoria"
        assert self.model._meta.verbose_name_plural == "Categorias"

    def test_field_cashflow(self):
        field = self.model._meta.get_field("cash_flow")
        CASH_FLOW_CHOICES = Choices(("revenue", "Receita"), ("expense", "Despesa"))

        assert field.max_length == 15
        assert field.blank is False
        assert field.null is False
        assert field.verbose_name == "Fluxo"
        assert field.choices == CASH_FLOW_CHOICES
        assert field.default == "expense"
        assert type(field) == models.CharField

    def test_field_description(self):
        field = self.model._meta.get_field("description")

        assert field.verbose_name == "Descrição"
        assert type(field) == models.CharField
        assert field.max_length == 200
        assert field.unique is True


def test_str(transaction_category):
    assert str(transaction_category) == "Some Category"
