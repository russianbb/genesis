from datetime import date

import factory


class ProjectFactory(factory.django.DjangoModelFactory):
    date = date(2020, 12, 31)
    category = "circularizacao"

    class Meta:
        model = "projects.Project"
