from finance.managers import RevenueManager
from finance.models import Revenue, Transaction
from utils.models import AbstractBaseModel


class TestRevenueModel:
    @classmethod
    def setup_class(cls):
        cls.model = Revenue

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True
        assert issubclass(self.model, Transaction) is True

    def test_meta(self):
        assert self.model._meta.proxy is True
        assert self.model._meta.verbose_name == "Transação Recebida"
        assert self.model._meta.verbose_name_plural == "Transações Recebidas"
        assert self.model._meta.managers_map["objects"].__class__ == RevenueManager
