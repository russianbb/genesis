import factory

from .cost_center import CostCenterFactory
from .transaction_category import TransactionCategoryFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    amount = factory.Faker("decimal")
    cost_center = factory.SubFactory(CostCenterFactory)
    category = factory.SubFactory(TransactionCategoryFactory)

    class Meta:
        model = "finance.Transaction"
