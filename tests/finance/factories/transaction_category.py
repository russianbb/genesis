import factory


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    description = "Some Category"
    cash_flow = "expense"

    class Meta:
        model = "finance.TransactionCategory"
