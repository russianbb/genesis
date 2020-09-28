from django.contrib import admin
from .models import Company, Store, Focal, Rtv
from .resources import (
    CompanyResource,
    StoreResource,
    FocalResource,
    RtvResource,
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin


@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource

    list_display = (
        'code_sap',
        'name',
        'fantasy',
        'system',
        'retroactive',
        'designated_name',
    )

    list_filter = (
        'designated',
        'system',
        'retroactive',
        'status',
    )

    search_fields = (
        'code_sap',
        'name',
        'fantasy',
    )

    filter_horizontal = ('rtv', 'focal')

    fieldsets = (
        ("Dados Cadastrais", {
            "fields": (
                'code_sap',
                'name',
                'fantasy',
                ('system', 'retroactive'),
            )
        }),
        ("Designado", {
            'fields': ('designated',)
        }),
        ("Contatos", {
            'fields': ('rtv', 'focal')
        }),
    )

    def designated_name(self, obj):
        return f'{obj.designated.get_full_name()}'

    designated_name.short_description = 'Designado'


@admin.register(Store)
class StoreAdmin(ImportExportModelAdmin):
    resource_class = StoreResource

    list_display = (
        'company',
        'code',
        'nickname',
        'document',
        'city',
        'state',    
        'inventory',
        'status',
    )

    fieldsets = (
        ("Dados Cadastrais", {
            "fields": (
                'company',
                'document',
                ('code','nickname'),
                ('contact', 'phone'),
                'email'
            )
        }),
        ("Localização", {
            'fields': (
                'address',
                ('city', 'state'),
                ('zipcode', 'ibge'),
                ('latitude', 'longitude')
            )
        }),
    )


@admin.register(Focal)
class FocalAdmin(ImportExportModelAdmin):
    resource_class = FocalResource

    list_display = (
        'name',
        'role',
        'email',
        'get_phone1',
        'get_phone2',
    )


@admin.register(Rtv)
class RtvAdmin(ImportExportModelAdmin):
    resource_class = RtvResource

    list_display = (
        'name',
        'email',
        'get_phone1',
        'get_phone2',
    )
