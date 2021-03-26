import pytest
from django.db import models
from finance.models import CostCenter
from utils.models import AbstractBaseModel

pytestmark = pytest.mark.django_db


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


def test_str(cost_center):
    assert str(cost_center) == "Some Cost Center"


def test_get_billings_amount(cost_center, invoice_received, invoice_not_received):
    assert float(cost_center.get_billings_amount) == 33.33


def test_get_billings_amount_null(cost_center):
    assert cost_center.get_billings_amount == "-"


def test_get_billings_not_received(cost_center, invoice_not_received):
    assert float(cost_center.get_billings_not_received) == 11.11


def test_get_billings_not_received_null(cost_center):
    assert cost_center.get_billings_not_received == "-"


def test_get_billings_received(cost_center, invoice_received):
    assert float(cost_center.get_billings_received) == 22.22


def test_get_billings_received_null(cost_center):
    assert cost_center.get_billings_received == "-"
