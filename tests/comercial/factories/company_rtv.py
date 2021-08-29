import factory

from .company import CompanyFactory
from .rtv import RtvFactory


class CompanyRtvFactory(factory.django.DjangoModelFactory):
    company = factory.SubFactory(CompanyFactory)
    rtv = factory.SubFactory(RtvFactory)

    class Meta:
        model = "comercial.CompanyRtv"
