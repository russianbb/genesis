from django.contrib import admin
from .models import Company, Store, Focal, CompanyFocal, Rtv, CompanyRtv
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
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

    def owner_name(self, obj):
        return f'{obj.owner.get_full_name()}'

    owner_name.short_description = 'Responsável Onix'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
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
class FocalAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'role',
        'email',
        'get_phone1',
        'get_phone2',
    )


@admin.register(CompanyFocal)
class CompanyFocalAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'focal',
    )

    fields = (
        'company',
        'focal',
        )


@admin.register(Rtv)
class RtvAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'get_phone1',
        'get_phone2',
    )


@admin.register(CompanyRtv)
class CompanyRtvAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'rtv',
    )

    fields = (
        'company',
        'rtv',
        )