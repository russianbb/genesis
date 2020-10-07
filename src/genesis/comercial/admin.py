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
        'trade_name',
        'fantasy_name',
        'system',
        'retroactive',
        'designated_name',
    )

    list_display_links = (
        'code_sap',
        'trade_name',
        'fantasy_name',
    )

    list_filter = (
        'designated',
        'system',
        'retroactive',
        'status',
    )

    search_fields = (
        'code_sap',
        'trade_name',
        'fantasy_name',
    )

    filter_horizontal = ('rtv', 'focal')

    fieldsets = (
        ("Dados Cadastrais", {
            "fields": (
                'code_sap',
                'trade_name',
                'fantasy_name',
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
        return obj.designated.get_full_name() or obj.designated.username

    designated_name.short_description = 'Designado'

    def get_queryset(self, request):
        queryset = super(CompanyAdmin, self).get_queryset(request)
        return queryset.select_related('designated')

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset.select_related('designated')

    def get_export_filename(self, request, queryset, file_format):
        filename = f'Distribuidores.{file_format.get_extension()}'
        return filename


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

    search_fields = (
        'company__trade_name',
        'company__fantasy_name',
        'document',
        'city',
        'state',
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

    def get_queryset(self, request):
        queryset = super(StoreAdmin, self).get_queryset(request)
        return queryset.select_related('company')

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset.select_related('company')

    def get_export_filename(self, request, queryset, file_format):
        filename = f'Filiais.{file_format.get_extension()}'
        return filename


@admin.register(Focal)
class FocalAdmin(ImportExportModelAdmin):
    resource_class = FocalResource

    list_display = ('name','role','email','get_phone1','get_phone2',)

    search_fields = ('name', 'email', 'phone1', 'phone2')

    fieldsets = (
        ("Dados do Responsável", {
            "fields": (
                'name',
                'role',
                ('phone1', 'phone2'),
                'email',
                'notes',
            )
        }),
    )

    # @TODO prefetch_relatade()
    def get_queryset(self, request):
        queryset = super(FocalAdmin, self).get_queryset(request)
        return queryset

    # @TODO prefetch_relatade()
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset

    def get_export_filename(self, request, queryset, file_format):
        filename = f'Responsaveis.{file_format.get_extension()}'
        return filename

@admin.register(Rtv)
class RtvAdmin(ImportExportModelAdmin):
    resource_class = RtvResource

    list_display = ('name', 'email', 'get_phone1', 'get_phone2')

    search_fields = ('name', 'email', 'phone1', 'phone2')

    fieldsets = (
        ("Dados do RTV", {
            "fields": (
                'name',
                ('phone1', 'phone2'),
                'email',
                'notes',
            )
        }),
    )

    # @TODO prefetch_relatade()
    def get_queryset(self, request):
        queryset = super(RtvAdmin, self).get_queryset(request)
        return queryset

    # @TODO prefetch_relatade()
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset

    def get_export_filename(self, request, queryset, file_format):
        filename = f'RTVs.{file_format.get_extension()}'
        return filename
