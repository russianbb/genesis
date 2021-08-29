import factory


class RtvFactory(factory.django.DjangoModelFactory):
    name = "Rtv"
    email = "rtv@teste.com.br"

    class Meta:
        model = "comercial.Rtv"
