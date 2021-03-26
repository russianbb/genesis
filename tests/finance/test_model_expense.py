from finance.managers import ExpenseManager
from finance.models import Expense, Transaction
from utils.models import AbstractBaseModel


class TestExpenseModel:
    @classmethod
    def setup_class(cls):
        cls.model = Expense

    def test_parent_class(self):
        assert issubclass(self.model, AbstractBaseModel) is True
        assert issubclass(self.model, Transaction) is True

    def test_meta(self):
        assert self.model._meta.proxy is True
        assert self.model._meta.verbose_name == "Transação Paga"
        assert self.model._meta.verbose_name_plural == "Transações Pagas"
        assert self.model._meta.managers_map["objects"].__class__ == ExpenseManager
