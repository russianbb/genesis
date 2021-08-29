import factory


class FocalFactory(factory.django.DjangoModelFactory):
    name = "Focal"
    email = "focal@teste.com.br"

    class Meta:
        model = "comercial.Focal"
