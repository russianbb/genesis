from django.contrib import admin

from .models import Category, CostCenter, Invoice, ServiceOrder, Transaction


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("category", "number", "amount", "issued_at")
    list_display_links = list_display
    search_fields = list_display
    list_filter = ("category", "issued_at")


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "updated_at")
    list_display_links = ("id", "description")
    search_fields = ("id", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "updated_at")
    list_display_links = ("id", "description")
    search_fields = ("id", "description")


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
