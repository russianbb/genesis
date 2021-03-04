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
        return f"{self.name}"


class Focal(AbstractBaseModel, ContactBaseModel):
    role = models.CharField(max_length=30, null=True, blank=True, verbose_name="Cargo")

    class Meta:
        ordering = ["status", "name"]
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return f"{self.name}"


class Company(AbstractBaseModel):
    code_sap = models.CharField(max_length=8, unique=True, verbose_name="Código SAP")
    company_name = models.CharField(max_length=100, verbose_name=_("Razão Social"))
    trade_name = models.CharField(max_length=100, verbose_name=_("Nome Fantasia"))
    SYSTEM_CHOICES = Choices(
        "Syagri", "Agrotis", "SAP", "Totvs", "Outros", "Não conhecido"
    )
    system = models.CharField(
        choices=SYSTEM_CHOICES,
        max_length=40,
        null=False,
        blank=False,
        verbose_name=_("ERP"),
        default="Não conhecido",
    )
    retroactive = models.BooleanField(
        default=False, null=True, blank=True, verbose_name=_("Retroativo"),
    )
    designated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Designado"),
        related_name="company",
    )
    rtv = models.ManyToManyField(
        Rtv, blank=True, related_name="company", through="CompanyRtv"
    )
    focal = models.ManyToManyField(
        Focal, blank=True, related_name="company", through="CompanyFocal"
    )

    class Meta:
        ordering = ["company_name"]
        verbose_name = "Distribuidor"
        verbose_name_plural = "Distribuidores"

    def __str__(self):
        return self.company_name


class Store(AbstractBaseModel, AddressBaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="stores",
        verbose_name="Distribuidor",
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
        ordering = ["status", "company__trade_name", "city", "nickname"]
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"
        unique_together = [["document", "code", "nickname", "company"]]

    def __str__(self):
        if self.code:
            return f"{self.company} - {self.code}"
        if self.nickname:
            return f"{self.company} - {self.nickname}"
        return f"{self.company} - {self.city}"

    def get_phone(self):
        if self.phone and len(self.phone) == 10:
            return f"({self.phone[:2]}) {self.phone[-8:-4]}-{self.phone[-4:]}"
        if self.phone and len(self.phone) == 11:
            return f"({self.phone[:2]}) {self.phone[-9:-4]}-{self.phone[-4:]}"
        return None

    def get_document(self):
        return f"{self.document[:2]}.{self.document[2:5]}.{self.document[5:8]}/{self.document[8:12]}-{self.document[12:14]}"  # noqa E501


class CompanyFocal(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Distribuidor"
    )
    focal = models.ForeignKey(
        Focal, on_delete=models.CASCADE, verbose_name="Responsável"
    )


class CompanyRtv(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Distribuidor"
    )
    rtv = models.ForeignKey(Rtv, on_delete=models.CASCADE, verbose_name="RTV")
