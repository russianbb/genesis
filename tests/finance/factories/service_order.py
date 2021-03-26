import factory


class ServiceOrderFactory(factory.django.DjangoModelFactory):
    description = "Some CostCenter"

    class Meta:
        model = "finance.ServiceOrder"
