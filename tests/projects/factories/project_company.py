import factory

from tests.comercial.factories import CompanyFactory

from .project import ProjectFactory


class ProjectCompanyFactory(factory.django.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    company = factory.SubFactory(CompanyFactory)

    class Meta:
        model = "projects.ProjectCompany"
