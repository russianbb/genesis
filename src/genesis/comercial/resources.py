from django.contrib.auth.models import User
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Company, Focal, Rtv, Store


class CompanyResource(resources.ModelResource):
    id = Field(attribute="pk", column_name="Id")
    code_sap = Field(attribute="code_sap", column_name="Código SAP")
    trade_name = Field(attribute="trade_name", column_name="Razão social")
    fantasy_name = Field(attribute="fantasy_name", column_name="Nome fantasia")
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
            "trade_name",
            "fantasy_name",
            "system",
            "retroactive",
            "designated_name",
            "status",
        )
        export_order = fields


class StoreResource(resources.ModelResource):
    id = Field(attribute="id", column_name="Id")
    company = Field(
        attribute="company",
        column_name="Razão social",
        widget=ForeignKeyWidget(Company),
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
    ibge = Field(attribute="ibge", column_name="Código IBGE")
    latitude = Field(attribute="latitude", column_name="Latitude")
    longitude = Field(attribute="longitude", column_name="Longitude")
    inventory = Field(attribute="inventory", column_name="Controla Estoque")
    status = Field(attribute="status", column_name="Ativo")

    class Meta:
        model = Store
        fields = (
            "id",
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
            "ibge",
            "latitude",
            "longitude",
            "inventory",
            "status",
        )
        export_order = fields


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
