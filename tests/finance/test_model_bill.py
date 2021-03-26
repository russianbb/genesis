from finance.managers import BillManager
from finance.models import Bill, Transaction
from utils.models import AbstractBaseModel


class TestBillModel:
    @classmethod
    def setup_class(cls):
        cls.model = Bill

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True
        assert issubclass(self.model, Transaction) is True

    def test_meta(self):
        assert self.model._meta.proxy is True
        assert self.model._meta.ordering == ["due_date", "id"]
        assert self.model._meta.verbose_name == "Transação a Pagar"
        assert self.model._meta.verbose_name_plural == "Transações a Pagar"
        assert self.model._meta.managers_map["objects"].__class__ == BillManager
