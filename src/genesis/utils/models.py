from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class AbstractBaseModel(models.Model):
    created_at = AutoCreatedField(verbose_name="Criado em")
    updated_at = AutoLastModifiedField(verbose_name="Atualizado em")
    status = models.BooleanField(verbose_name=_("Ativo"), default=True)

    class Meta:
        abstract = True


class AddressBaseModel(models.Model):
    address = models.CharField(
        blank=True, null=False, verbose_name=_("Endereço"), max_length=254, default="",
    )
    city = models.CharField(
        blank=False, null=False, verbose_name=_("Cidade"), max_length=100, default="",
    )
    state = models.CharField(
        blank=False, null=False, verbose_name=_("Estado"), max_length=2, default="",
    )
    zipcode = models.CharField(
        blank=True, null=False, verbose_name=_("CEP"), max_length=10, default="",
    )
    ibge = models.CharField(
        blank=True, null=False, verbose_name=_("IBGE"), max_length=9
    )
    latitude = models.CharField(
        blank=True, null=True, verbose_name=_("Latitude"), max_length=50,
    )
    longitude = models.CharField(
        blank=True, null=True, verbose_name=_("Longitude"), max_length=50,
    )

    class Meta:
        abstract = True


class ContactBaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    phone1 = models.CharField(
        max_length=11, null=True, blank=True, verbose_name="Telefone"
    )
    phone2 = models.CharField(
        max_length=11, null=True, blank=True, verbose_name="Telefone"
    )
    notes = models.TextField(null=True, blank=True, verbose_name="Anotações")

    def get_phone1(self):
        if self.phone1 and len(self.phone1) == 10:
            return f"({self.phone1[:2]}) {self.phone1[-8:-4]}-{self.phone1[-4:]}"
        if self.phone1 and len(self.phone1) == 11:
            return f"({self.phone1[:2]}) {self.phone1[-9:-4]}-{self.phone1[-4:]}"
        return None

    get_phone1.short_description = "Telefone Principal"

    def get_phone2(self):
        if self.phone2 and len(self.phone2) == 10:
            return f"({self.phone2[:2]}) {self.phone2[-8:-4]}-{self.phone2[-4:]}"
        if self.phone2 and len(self.phone2) == 11:
            return f"({self.phone2[:2]}) {self.phone2[-9:-4]}-{self.phone2[-4:]}"
        return None

    get_phone2.short_description = "Telefone Secundario"

    class Meta:
        abstract = True


class AbstractStockModel(models.Model):
    owned = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="EF",
        help_text="Saldo de estoque físico",
        null=True,
        blank=True,
    )
    sold = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="VEF",
        help_text="Saldo de venda para entrega futura faturada com CFOP 5922, 6922",
        null=True,
        blank=True,
    )
    sent = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="Em Terceiros",
        help_text="Saldo de estoque físico do distribuidor armazenado em poder de terceiros (Remessa para enviada)",  # noqa: E501
        null=True,
        blank=True,
    )
    received = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="De Terceiros",
        help_text="Saldo de estoque físico de terceiros armazenado em poder do distribuidor (Remessa recebida)",  # noqa: E501
        null=True,
        blank=True,
    )
    transit = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="Em Trânsito",
        help_text="Saldo de estoque físico em trânsito",
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        verbose_name="Saldo Calculado",
        help_text="Saldo de estoque calculado. Saldo = EF - VEF + Em Terceiros - De Terceiros +- Transito",  # noqa: E501
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class UploadTo:
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, instance, filename):
        return f"{self.base_path}/{instance.category}/{filename}"

    def deconstruct(self):
        return ("utils.models.UploadTo", [self.base_path], {})
