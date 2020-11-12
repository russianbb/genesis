from comercial.models import Company
from django.db import models
from utils.models import AbstractBaseModel


class Project(AbstractBaseModel):
    PROJECT_CHOICES = (
        ("circularizacao", "Circularização de Estoque"),
        ("inventario", "Inventário Físico"),
        ("outros", "Outros"),
    )

    date = models.DateField(
        verbose_name="Data Base", help_text="Data de mensuração do estoque"
    )
    company = models.ManyToManyField(
        Company, related_name="project", through="ProjectCompany"
    )
    category = models.CharField(
        verbose_name="Tipo de projeto", max_length=200, choices=PROJECT_CHOICES,
    )

    class Meta:
        ordering = ("date",)
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        unique_together = ("date", "category")

    def __str__(self):
        return f'{self.get_category_display()} - {self.date.strftime("%d/%m/%y")}'


class ProjectCompany(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Projeto"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Distribuidor"
    )

    class Meta:
        ordering = ("project", "company")
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        unique_together = ("project", "company")
