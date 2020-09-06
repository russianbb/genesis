from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.choices import Choices
from utils import AbstractBaseModel, AddressBaseModel, ContactBaseModel

# Create your models here


class Company(AbstractBaseModel):
    code_sap = models.CharField(max_length=8, unique=True)
    company_name = models.CharField(max_length=100, verbose_name=_("Razão Social"))
    fantasy_name = models.CharField(max_length=100, verbose_name=_("Nome Fantasia"))
    SYSTEM_CHOICES = Choices(
        'Syagri', 'Agrotis', 'SAP', 'Totvs', 'Outros'
    )
    system = models.CharField(
        max_length=40, choices=SYSTEM_CHOICES, verbose_name=_("ERP")
    )
    retroactive = models.BooleanField(
        default=False, verbose_name=_('Relatorio Retroativo')
    )
    resp = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["company_name"]
        verbose_name = "Distribuidor"
        verbose_name_plural = "Distribuidores"


class Store(AbstractBaseModel, AddressBaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="stores"
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
        ordering = ["company__company_name", "city", "nickname"]
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"
        unique_together = [["document", "code", "nickname", "company"]]


class Focal(AbstractBaseModel, ContactBaseModel):
    role = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"


class CompanyFocal(AbstractBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    focal = models.ForeignKey(Focal, on_delete=models.CASCADE)

    class Meta:
        ordering = ["company__company_name", "focal__name"]
        unique_together = ("company", "focal")
        verbose_name = "Responsável pelo Distribuidor"
        verbose_name_plural = "Responsável pelo Distribuidor"


class Rtv(AbstractBaseModel, ContactBaseModel):
    class Meta:
        ordering = ["name"]
        verbose_name = "Rtv"
        verbose_name_plural = "Rtvs"


class CompanyRtv(AbstractBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rtv = models.ForeignKey(Rtv, on_delete=models.CASCADE)

    class Meta:
        ordering = ["company__company_name", "rtv__name"]
        unique_together = ("company", "rtv")
        verbose_name = "Rtv do Distribuidor"
        verbose_name_plural = "Rtvs do Distribuidores"
