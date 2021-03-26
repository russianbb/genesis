from django.db import models
from finance.models import ServiceOrder
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
