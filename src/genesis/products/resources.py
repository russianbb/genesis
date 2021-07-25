from django.utils import formats
from import_export import resources
from import_export.fields import Field

from .models import CompanyProduct, OnixProduct, SyngentaProduct


class OnixProductResource(resources.ModelResource):
    id = Field(attribute="pk", column_name="Id")
    description = Field(attribute="description", column_name="Descrição completa")
    prefix = Field(attribute="prefix", column_name="Nome do produto")
    unit_size = Field(attribute="unit_size", column_name="Tamanho da embalagem")
    unit_mesure = Field(attribute="unit_mesure", column_name="Tipo de unidade")
    unit_volume = Field(attribute="unit_volume", column_name="Volume")
    status = Field(attribute="status", column_name="Status")

    class Meta:
        model = OnixProduct
        fields = (
            "id",
            "description",
            "prefix",
            "unit_size",
            "unit_mesure",
            "unit_volume",
            "status",
        )
        export_order = fields

    def dehydrate_unit_size(self, obj):
        return formats.number_format(obj.unit_size, 0)

    def dehydrate_unit_volume(self, obj):
        return formats.number_format(obj.unit_volume, 4)

    def dehydrate_status(self, obj):
        return "Ativo" if obj.status else "Inativo"


class SyngentaProductResource(resources.ModelResource):
    agicode = Field(attribute="agicode", column_name="Agicode")
    family = Field(attribute="family", column_name="Família")
    description = Field(attribute="description", column_name="Descrição")
    status = Field(attribute="status", column_name="Status")
    onix = Field(attribute="onix__pk", column_name="Id Onix")
    onix_description = Field(attribute="onix__description", column_name="Produto Onix")
    onix_unit_volume = Field(attribute="onix__unit_volume", column_name="Volume")

    class Meta:
        model = SyngentaProduct
        fields = (
            "agicode",
            "family",
            "description",
            "status",
            "onix",
            "onix_description",
            "onix_unit_volume",
        )
        export_order = fields

    def dehydrate_onix_unit_volume(self, obj):
        return formats.number_format(obj.onix.unit_volume, 4)

    def dehydrate_status(self, obj):
        return "Ativo" if obj.status else "Inativo"


class CompanyProductResource(resources.ModelResource):
    company = Field(attribute="company", column_name="Distribuidor")
    code = Field(attribute="code", column_name="Código")
    description = Field(attribute="description", column_name="Descrição")
    status = Field(attribute="status", column_name="Status")
    onix = Field(attribute="onix__id", column_name="Id Onix")
    onix_description = Field(attribute="onix__description", column_name="Produto Onix")
    onix_unit_volume = Field(attribute="onix__unit_volume", column_name="Volume")

    class Meta:
        model = CompanyProduct
        fields = (
            "company",
            "code",
            "description",
            "onix",
            "onix_description",
            "onix_unit_volume",
        )
        export_order = fields

    def dehydrate_onix_unit_volume(self, obj):
        return formats.number_format(obj.onix.unit_volume, 4)

    def dehydrate_status(self, obj):
        return "Ativo" if obj.status else "Inativo"
