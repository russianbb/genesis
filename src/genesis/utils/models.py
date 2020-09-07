from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = AutoCreatedField(verbose_name="criado em")
    updated_at = AutoLastModifiedField(verbose_name="atualizado em")
    status = models.BooleanField(verbose_name=_("Ativo"), default=True)

    class Meta:
        abstract = True


class AddressBaseModel(models.Model):
    address = models.CharField(
        blank=True, null=False, verbose_name=_("Endereço"), max_length=100, default="",
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
    code_ibge = models.CharField(
        blank=True, null=False, verbose_name=_("Código IBGE"), max_length=9
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
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    phone1 = models.CharField(
        max_length=11, null=True, blank=True, verbose_name=_("Telefone")
    )
    phone2 = models.CharField(
        max_length=11, null=True, blank=True, verbose_name=_("Telefone")
    )
    notes = models.TextField(null=True, blank=True)

    def get_phone1(self):
        if self.phone1:
            return f"({self.phone1[:2]}) {self.phone1[-11:-6]}-{self.phone1[-6:-2]}"

    get_phone1.short_description = "Telefone Principal"

    def get_phone2(self):
        if self.phone2:
            return f"({self.phone2[:2]}) {self.phone2[-11:-6]}-{self.phone2[-6:-2]}"

    get_phone2.short_description = "Telefone Secundario"

    class Meta:
        abstract = True
