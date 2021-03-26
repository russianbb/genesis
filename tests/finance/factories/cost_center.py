import factory


class CostCenterFactory(factory.django.DjangoModelFactory):
    description = "Some CostCenter"

    class Meta:
        model = "finance.CostCenter"
