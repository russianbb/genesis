from django.contrib import admin
from utils.admin import ReadOnlyAdminMixin
from utils.constants import CATEGORY_DIVIDENDS

from .models import Category, CostCenter, Invoice, ServiceOrder, Transaction


class InvoiceInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Invoice
    fields = ("amount", "category", "issued_at")
    readonly_fields = fields
    extra = 0


class PaidInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Transaction
    fields = ("amount", "category", "transacted_at")
    readonly_fields = fields
    extra = 0
    verbose_name = "Recebido"
    verbose_name_plural = "Recebidos"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__cash_flow="receipt")


class DividendsInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Transaction
    fields = ("amount", "category", "transacted_at")
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


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "category", "amount", "issued_at")
    list_display_links = list_display
    search_fields = list_display
    list_filter = ("category", "issued_at")


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
        "amount",
        "transacted_at",
    )
    list_display_links = list_display
    search_fields = list_display
    list_filter = ("category", "cost_center", "transacted_at")
