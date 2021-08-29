import factory

from .company import CompanyFactory
from .focal import FocalFactory


class CompanyFocalFactory(factory.django.DjangoModelFactory):
    company = factory.SubFactory(CompanyFactory)
    focal = factory.SubFactory(FocalFactory)

    class Meta:
        model = "comercial.CompanyFocal"
