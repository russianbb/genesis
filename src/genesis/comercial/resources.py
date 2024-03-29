from django.contrib.auth.models import User
from django.utils import formats
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Company, CompanyFocal, CompanyRtv, Focal, Rtv, Store


class CompanyResource(resources.ModelResource):
    id = Field(attribute="pk", column_name="Id")
    code_sap = Field(attribute="code_sap", column_name="Código SAP")
    company_name = Field(attribute="company_name", column_name="Razão social")
    trade_name = Field(attribute="trade_name", column_name="Nome fantasia")
    system = Field(attribute="system", column_name="ERP")
    retroactive = Field(attribute="retroactive", column_name="Retroativo")
    designated_name = Field(
        attribute="designated",
        column_name="Designado Onix",
        widget=ForeignKeyWidget(User, "username"),
    )
    status = Field(attribute="status", column_name="Ativo")

    class Meta:
        model = Company
        fields = (
            "id",
            "code_sap",
            "company_name",
            "trade_name",
            "system",
            "retroactive",
            "designated_name",
            "status",
        )
        export_order = fields


class StoreResource(resources.ModelResource):
    code_sap = Field(attribute="company__code_sap", column_name="Codigo SAP")
    company_name = Field(attribute="company__company_name", column_name="Razão social",)
    trade_name = Field(attribute="company__trade_name", column_name="Nome Fantasia")
    id = Field(attribute="id", column_name="Id")
    code = Field(attribute="code", column_name="Código da filial")
    nickname = Field(attribute="nickname", column_name="Apelido da filial")
    document = Field(attribute="document", column_name="CNPJ")
    contact = Field(attribute="contact", column_name="Contato")
    phone = Field(attribute="phone", column_name="Telefone")
    email = Field(attribute="email", column_name="E-mail")
    city = Field(attribute="city", column_name="Cidade")
    state = Field(attribute="state", column_name="Estado")
    address = Field(attribute="address", column_name="Endereço")
    ibge = Field(attribute="ibge", column_name="Código IBGE")
    latitude = Field(attribute="latitude", column_name="Latitude")
    longitude = Field(attribute="longitude", column_name="Longitude")
    inventory = Field(attribute="inventory", column_name="Controla Estoque")
    status = Field(attribute="status", column_name="Ativo")

    class Meta:
        model = Store
        fields = (
            "code_sap",
            "company_name",
            "trade_name",
            "id",
            "code",
            "nickname",
            "document",
            "contact",
            "phone",
            "email",
            "city",
            "state",
            "address",
            "ibge",
            "latitude",
            "longitude",
            "inventory",
            "status",
        )
        export_order = fields

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company")

    def dehydrate_status(self, obj):
        if obj.status:
            return "Sim"
        return "Não"

    def dehydrate_inventory(self, obj):
        if obj.inventory:
            return "Sim"
        return "Não"

    def dehydrate_latitude(self, obj):
        latitude = float(obj.latitude or 0)
        return formats.number_format(latitude, 6)

    def dehydrate_longitude(self, obj):
        longitude = float(obj.longitude or 0)
        return formats.number_format(longitude, 6)


class FocalResource(resources.ModelResource):
    id = Field(attribute="id", column_name="Id")
    name = Field(attribute="name", column_name="Nome")
    role = Field(attribute="role", column_name="Cargo")
    phone1 = Field(attribute="get_phone1", column_name="Telefone principal")
    phone2 = Field(attribute="get_phone2", column_name="Telefone secundário")
    email = Field(attribute="email", column_name="E-mail")
    notes = Field(attribute="notes", column_name="Anotação")

    class Meta:
        model = Focal
        fields = (
            "id",
            "name",
            "role",
            "phone1",
            "phone2",
            "email",
            "notes",
        )
        export_order = fields


class RtvResource(resources.ModelResource):
    id = Field(attribute="id", column_name="Id")
    name = Field(attribute="name", column_name="Nome")
    phone1 = Field(attribute="get_phone1", column_name="Telefone principal")
    phone2 = Field(attribute="get_phone2", column_name="Telefone secundário")
    email = Field(attribute="email", column_name="E-mail")
    notes = Field(attribute="notes", column_name="Anotação")

    class Meta:
        model = Rtv
        fields = (
            "id",
            "name",
            "phone1",
            "phone2",
            "email",
            "notes",
        )
        export_order = fields


class StorePublicResource(resources.ModelResource):
    company = Field(
        attribute="company",
        column_name="Razão social",
        widget=ForeignKeyWidget(Company, "trade_name"),
    )
    code = Field(attribute="code", column_name="Código da filial")
    nickname = Field(attribute="nickname", column_name="Apelido da filial")
    document = Field(attribute="document", column_name="CNPJ")
    contact = Field(attribute="contact", column_name="Contato")
    phone = Field(attribute="phone", column_name="Telefone")
    email = Field(attribute="email", column_name="E-mail")
    city = Field(attribute="city", column_name="Cidade")
    state = Field(attribute="state", column_name="Estado")
    address = Field(attribute="address", column_name="Endereço")
    status = Field(attribute="status", column_name="Ativo")

    def __init__(self, company):
        self.company = company

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(company=self.company).select_related("company")

    class Meta:
        model = Store
        fields = (
            "company",
            "code",
            "nickname",
            "document",
            "contact",
            "phone",
            "email",
            "city",
            "state",
            "address",
            "status",
        )
        export_order = fields

    def dehydrate_status(self, obj):
        if obj.status:
            return "Sim"
        return "Não"


class CompanyRtvResource(resources.ModelResource):
    code_sap = Field(attribute="company__code_sap", column_name="Código SAP")
    company_name = Field(attribute="company__company_name", column_name="Razão social")
    trade_name = Field(attribute="company__trade_name", column_name="Nome fantasia")
    name = Field(attribute="rtv__name", column_name="Nome")
    email = Field(attribute="rtv__email", column_name="E-mail")
    phone1 = Field(attribute="rtv__get_phone1", column_name="Telefone principal")
    phone2 = Field(attribute="rtv__get_phone2", column_name="Telefone secundário")
    notes = Field(attribute="rtv__notes", column_name="Anotação")
    status = Field(attribute="rtv__status", column_name="Ativo")

    class Meta:
        model = CompanyRtv
        fields = (
            "code_sap",
            "company_name",
            "trade_name",
            "name",
            "email",
            "phone1",
            "phone2",
            "notes",
            "status",
        )
        export_order = fields

    def dehydrate_status(self, obj):
        if obj.rtv.status:
            return "Sim"
        return "Não"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company", "rtv")


class CompanyFocalResource(resources.ModelResource):
    code_sap = Field(attribute="company__code_sap", column_name="Código SAP")
    company_name = Field(attribute="company__company_name", column_name="Razão social")
    trade_name = Field(attribute="company__trade_name", column_name="Nome fantasia")
    name = Field(attribute="focal__name", column_name="Nome")
    role = Field(attribute="focal__role", column_name="Cargo")
    email = Field(attribute="focal__email", column_name="E-mail")
    phone1 = Field(attribute="focal__get_phone1", column_name="Telefone principal")
    phone2 = Field(attribute="focal__get_phone2", column_name="Telefone secundário")
    notes = Field(attribute="focal__notes", column_name="Anotação")
    status = Field(attribute="focal__status", column_name="Ativo")

    class Meta:
        model = CompanyFocal
        fields = (
            "code_sap",
            "company_name",
            "trade_name",
            "name",
            "role",
            "email",
            "phone1",
            "phone2",
            "notes",
            "status",
        )
        export_order = fields

    def dehydrate_status(self, obj):
        if obj.focal.status:
            return "Sim"
        return "Não"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company", "focal")
