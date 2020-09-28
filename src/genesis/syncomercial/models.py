from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.choices import Choices
from utils.models import AbstractBaseModel, AddressBaseModel, ContactBaseModel


class Rtv(AbstractBaseModel, ContactBaseModel):
    class Meta:
        ordering = ["status", "name"]
        verbose_name = "Rtv"
        verbose_name_plural = "Rtvs"

    def __str__(self):
        return f'{self.name}'


class Focal(AbstractBaseModel, ContactBaseModel):
    role = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='Cargo')

    class Meta:
        ordering = ["status", "name"]
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return f'{self.name}'


class Company(AbstractBaseModel):
    code_sap = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=100, verbose_name=_("Razão Social"))
    fantasy = models.CharField(max_length=100, verbose_name=_("Nome Fantasia"))
    SYSTEM_CHOICES = Choices(
        'Syagri',
        'Agrotis',
        'SAP',
        'Totvs',
        'Outros'
    )
    system = models.CharField(
        choices=SYSTEM_CHOICES,
        max_length=40,
        null=True,
        blank=True,
        verbose_name=_("ERP"),
    )
    retroactive = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name=_('Relatorio Retroativo'),
    )
    designated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Designado")
    )
    rtv = models.ManyToManyField(
        Rtv,
        blank=True,
        related_name = "rtv",
        )
    focal = models.ManyToManyField(
        Focal,
        blank=True,
        related_name = "focal"
        )

    class Meta:
        ordering = ["name"]
        verbose_name = "Distribuidor"
        verbose_name_plural = "Distribuidores"

    def __str__(self):
        return self.name

class Store(AbstractBaseModel, AddressBaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="stores", verbose_name='Distribuidor',
    )
    code = models.CharField(
        max_length=15, null=True, blank=True, verbose_name=_("Código")
    )
    nickname = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Apelido")
    )
    document = models.CharField(max_length=14, verbose_name=_("CNPJ"))
    contact = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Contato")
    )
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    phone = models.CharField(
        max_length=11, null=True, blank=True, verbose_name=_("Telefone")
    )
    inventory = models.BooleanField(
        default=True, null=False, blank=False, verbose_name=_("Controla Estoque")
    )

    class Meta:
        ordering = ["status", "company__name", "city", "nickname"]
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"
        unique_together = [["document", "code", "nickname", "company"]]

    def __str__(self):
        if self.code:
            return f'{self.company} - {self.code}'
        if self.name:
            return f'{self.company} - {self.name}'
        return f'{self.company} - {self.city}'
