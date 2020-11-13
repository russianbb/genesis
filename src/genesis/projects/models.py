from comercial.models import Company
from django.db import models
from model_utils.fields import MonitorField
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
    report_request = models.BooleanField(
        verbose_name="Solicitação de relatórios", default=False
    )
    report_request_changed = MonitorField(
        monitor="report_request", verbose_name="Solicitação de relatórios em"
    )

    report_response = models.BooleanField(
        verbose_name="Recebimento dos relatórios", default=False
    )
    report_response_changed = MonitorField(
        monitor="report_response", verbose_name="Recebimento dos relatórios em"
    )

    manipulated = models.BooleanField(verbose_name="Modelo consolidado", default=False)
    manipulated_changed = MonitorField(
        monitor="manipulated", verbose_name="Modelo consolidado em"
    )

    justification_sent = models.BooleanField(
        verbose_name="Justificativas enviadas", default=False
    )
    justification_sent_changed = MonitorField(
        monitor="justification_sent", verbose_name="Justificativas enviadas em"
    )

    justification_received = models.BooleanField(
        verbose_name="Justificativas recebidas", default=False
    )
    justification_received_changed = MonitorField(
        monitor="justification_received", verbose_name="Justificativas recebidas em"
    )

    justification_validated = models.BooleanField(
        verbose_name="Justificativas validadas", default=False
    )
    justification_validated_changed = MonitorField(
        monitor="justification_validated", verbose_name="Justificativas validadas em"
    )

    letter_sent = models.BooleanField(verbose_name="Envio da carta", default=False)
    letter_sent_changed = MonitorField(
        monitor="letter_sent", verbose_name="Envio da carta em"
    )

    retter_received = models.BooleanField(
        verbose_name="Recebimento da carta", default=False
    )
    retter_received_changed = MonitorField(
        monitor="retter_received", verbose_name="Recebimento da carta em"
    )

    class Meta:
        ordering = ("project", "company")
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        unique_together = ("project", "company")

    def __str__(self):
        return f"{self.project} - {self.company}"
