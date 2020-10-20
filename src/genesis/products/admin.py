from django.contrib import admin
from import_export.admin import ExportMixin

from .models import CompanyProduct, OnixProduct, SyngentaProduct
from .resources import (
    CompanyProductResource,
    OnixProductResource,
    SyngentaProductResource,
)


class SyngentaProductInline(admin.TabularInline):
    model = SyngentaProduct
    extra = 0
    max_num = 0
    can_delete = False


@admin.register(OnixProduct)
class OnixProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OnixProductResource
    list_display = (
        "id",
        "description",
        "prefix",
        "unit_size",
        "unit_mesure",
        "unit_volume",
    )
    list_display_links = ("description",)
    search_fields = (
        "id",
        "description",
        "prefix",
        "unit_size",
        "unit_mesure",
        "unit_volume",
    )
    list_filter = ("unit_size", "unit_mesure", "unit_volume")
    fields = (
        "prefix",
        "unit_size",
        "unit_mesure",
        "unit_volume",
        "description",
        "status",
    )

    inlines = [SyngentaProductInline]

    def get_export_filename(self, request, queryset, file_format):
        filename = f"ProdutosOnix.{file_format.get_extension()}"
        return filename


@admin.register(SyngentaProduct)
class SyngentaProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SyngentaProductResource
    list_display = (
        "agicode",
        "description",
        "family",
        "get_onix_id",
        "get_onix_description",
        "updated_at",
    )
    list_display_links = ("agicode", "description")
    search_fields = ("agicode", "description", "family")
    fields = ("onix", "agicode", "family", "description", "status")

    def get_onix_description(self, obj):
        return obj.onix

    get_onix_description.short_description = "Produto Onix"

    def get_onix_id(self, obj):
        return obj.onix.pk

    get_onix_id.short_description = "Id Onix"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("onix")

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset.select_related("onix")

    def get_export_filename(self, request, queryset, file_format):
        filename = f"ProdutosSyngenta.{file_format.get_extension()}"
        return filename


@admin.register(CompanyProduct)
class CompanyProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CompanyProductResource
    list_display = (
        "company",
        "code",
        "description",
        "get_onix_id",
        "get_onix_description",
        "updated_at",
    )
    list_display_links = ("code", "description")
    search_fields = (
        "company__trade_name",
        "company__fantasy_name",
        "code",
        "description",
        "onix__pk",
        "onix__description",
    )
    fields = ("onix", "company", "code", "description", "status")

    def get_onix_id(self, obj):
        return obj.onix.pk

    get_onix_id.short_description = "Id Onix"

    def get_onix_description(self, obj):
        return obj.onix.description

    get_onix_description.short_description = "Produto Onix"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("onix", "company")

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        return queryset.select_related("onix", "company")

    def get_export_filename(self, request, queryset, file_format):
        filename = f"ProdutosDistribuidor.{file_format.get_extension()}"
        return filename
