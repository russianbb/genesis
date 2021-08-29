from datetime import date

import factory


class ProjectFactory(factory.django.DjangoModelFactory):
    date = date(1988, 1, 31)
    category = "circularizacao"

    class Meta:
        model = "projects.Project"
