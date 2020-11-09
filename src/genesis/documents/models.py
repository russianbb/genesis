from comercial.models import Company
from django.db import models
from projects.models import Project
from utils.models import AbstractBaseModel


# Create your models here.
class Document(AbstractBaseModel):
    CATEGORY_CHOICES = (
        ("import", "Modelo de Importação"),
        ("justification", "Modelo de Justificativas"),
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name="Projeto",
        related_name="document",
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name="Distribuidor",
        related_name="document",
    )
    category = models.CharField(
        verbose_name="Tipo de Documento", max_length=100, choices=CATEGORY_CHOICES,
    )
    file = models.FileField(verbose_name="Arquivo", upload_to="stock/")

    class Meta:
        ordering = ("project", "company", "category")
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        unique_together = ("project", "company", "category")

    def __str__(self):
        return f"{self.project} - {self.company.company_name}"
