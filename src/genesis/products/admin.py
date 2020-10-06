from django.contrib import admin

# Register your models here.
from .models import OnixProduct, SyngentaProduct, CompanyProduct


class SyngentaProductInline(admin.TabularInline):
    model = SyngentaProduct
    extra = 0
    max_num = 0
    can_delete = False


@admin.register(OnixProduct)
class OnixProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'created_at')
    list_display_links = ('description',)
    search_fields = ('pk', 'description', 'prefix', 'unit_size', 'unit_mesure', 'unit_volume')
    list_filter = ('unit_size', 'unit_mesure', 'unit_volume')
    fields = ('prefix', 'unit_size', 'unit_mesure', 'unit_volume', 'description', 'status')

    inlines = [SyngentaProductInline]


@admin.register(SyngentaProduct)
class SyngentaProductAdmin(admin.ModelAdmin):
    list_display = ('agicode', 'description', 'family', 'get_product_onix', 'get_product_onix_description', 'updated_at')
    list_display_links = ('agicode', 'description')
    search_fields = ('agicode', 'description', 'family')
    fields = ('product_onix', 'agicode', 'family', 'description', 'status')

    def get_product_onix(self, obj):
        return obj.product_onix.pk

    def get_product_onix_description(self, obj):
        return obj.product_onix.pk


@admin.register(CompanyProduct)
class CompanyProductAdmin(admin.ModelAdmin):
    list_display = ('company', 'code', 'description', 'get_product_onix', 'get_product_onix_description', 'updated_at')
    list_display_links = ('code', 'description')
    search_fields = ('company', 'code', 'description', 'product_onix__pk', 'product_onix__description')
    fields = ('product_onix', 'company', 'code', 'description', 'status')

    def get_product_onix(self, obj):
        return obj.product_onix.pk

    def get_product_onix_description(self, obj):
        return obj.product_onix.pk