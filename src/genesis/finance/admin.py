from django.contrib import admin
from utils.admin import ReadOnlyAdminMixin
from utils.constants import CATEGORY_DIVIDENDS

from .models import Category, CostCenter, Invoice, ServiceOrder, Transaction


class InvoiceInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Invoice
    fields = ("get_amount_display", "category", "issued_at")
    readonly_fields = fields
    extra = 0

    def get_amount_display(self, obj):
        return obj.get_amount_display

    get_amount_display.short_description = "Valor"


class PaidInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Transaction
    fields = ("get_amount_display", "category", "transacted_at")
    readonly_fields = fields
    extra = 0
    verbose_name = "Recebido"
    verbose_name_plural = "Recebidos"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__cash_flow="receipt")

    def get_amount_display(self, obj):
        return obj.get_amount_display

    get_amount_display.short_description = "Valor"


class DividendsInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Transaction
    fields = ("get_amount_display", "category", "transacted_at")
    readonly_fields = fields
    extra = 0
    verbose_name = "Dividendos Pagos"
    verbose_name_plural = "Dividendos Pagos"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(
            category__cash_flow=CATEGORY_DIVIDENDS["cash_flow"],
            category__description=CATEGORY_DIVIDENDS["description"],
        )

    def get_amount_display(self, obj):
        return obj.get_amount_display

    get_amount_display.short_description = "Valor"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "get_number_display",
        "category",
        "get_amount_display",
        "cost_center",
        "issued_at",
    )
    list_display_links = list_display
    search_fields = list_display
    list_filter = ("category", "issued_at")

    def get_amount_display(self, obj):
        return obj.get_amount_display

    get_amount_display.short_description = "Valor"

    def get_number_display(self, obj):
        return obj.get_number_display

    get_number_display.short_description = "Número"


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "updated_at")
    list_display_links = ("id", "description")
    search_fields = ("id", "description")
    inlines = (InvoiceInline, PaidInline, DividendsInline)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "cash_flow", "description", "updated_at")
    list_display_links = ("id", "cash_flow", "description")
    search_fields = ("id", "description")
    list_filter = ("cash_flow",)


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "buy_order", "updated_at")
    list_display_links = ("id", "description")
    search_fields = ("id", "description", "buy_order")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "cost_center",
        "get_amount_display",
        "transacted_at",
    )
    list_display_links = list_display
    search_fields = (
        "id",
        "category__description",
        "cost_center__description",
        "notes",
        "amount",
    )
    list_filter = ("category", "cost_center", "transacted_at")
