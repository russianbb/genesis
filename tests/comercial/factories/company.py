import factory


class CompanyFactory(factory.django.DjangoModelFactory):
    code_sap = "12345678"
    company_name = "Republica Jabuti LTDA ME"
    trade_name = "Rep Jabuti"
    system = "Outros"
    retroactive = False

    class Meta:
        model = "comercial.Company"
