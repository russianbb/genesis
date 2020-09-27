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
        'owner_name',
    )

    fields = (
        'code_sap',
        'name',
        'fantasy',
        'system',
        'retroactive',
        'owner',
        'rtv',
        'focal',
    )

    list_filter = (
        'owner',
        'system',
        'retroactive',
        'status',
    )

    search_fields = (
        'code_sap',
        'name',
        'fantasy',
    )

    filter_vertical = ('rtv', 'focal')

    def owner_name(self, obj):
        return f'{obj.owner.get_full_name()}'

    owner_name.short_description = 'Responsável Onix'


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
