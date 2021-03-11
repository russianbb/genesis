from datetime import datetime

import factory

from . import CostCenterFactory, ServiceOrderFactory


class InvoiceFactory(factory.django.DjangoModelFactory):
    number = factory.Faker("integer")
    amount = factory.Faker("decimal")
    category = "invoice"
    issued_at = datetime.now()
    service_order = factory.SubFactory(ServiceOrderFactory)
    cost_center = factory.SubFactory(CostCenterFactory)

    class Meta:
        model = "finance.Receivable"
