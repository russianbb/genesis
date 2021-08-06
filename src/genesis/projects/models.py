from django.db import models
from utils.models import AbstractBaseModel

PROJECT_CHOICES = (
    ("circularizacao", "Circularização de Estoque"),
    ("inventario", "Inventário Físico"),
)


class Project(AbstractBaseModel):
    date = models.DateField(
        verbose_name="Data Base", help_text="Data de mensuração do estoque"
    )
    companies = models.ManyToManyField(
        "comercial.Company", related_name="projects", through="ProjectCompany"
    )
    category = models.CharField(
        verbose_name="Tipo de projeto", max_length=200, choices=PROJECT_CHOICES,
    )

    class Meta:
        ordering = ("-date",)
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        unique_together = ("date", "category")

    def __str__(self):
        return f"{self.date_display} - {self.get_category_display()}"

    @property
    def date_display(self):
        return self.date.strftime("%d/%m/%Y")


class ProjectCompany(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Projeto"
    )
    company = models.ForeignKey(
        "comercial.Company", on_delete=models.CASCADE, verbose_name="Distribuidor"
    )

    class Meta:
        ordering = ("-project", "company__trade_name")
        verbose_name = "distribuidor do drojeto"
        verbose_name_plural = "distribuidores do drojeto"
        unique_together = ("project", "company")

    def __str__(self):
        return f"{self.project} - {self.company}"