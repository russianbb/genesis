from django.contrib import admin

from .models import Index, Item, Justification, SyngentaBalance


@admin.register(SyngentaBalance)
class SyngentaBalanceAdmin(admin.ModelAdmin):
    list_display = ("project", "company", "product", "balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "product", "balance")

    fieldsets = (
        ("Saldo Syngenta", {"fields": ("project", "company", "product", "balance",)},),
    )

    class Meta:
        fields = "__all__"


@admin.register(Justification)
class JustificationAdmin(admin.ModelAdmin):
    list_display = ("project", "company", "product", "description")
    list_display_links = ("description",)
    search_fields = ("company", "product")

    fieldsets = (
        (
            "Justificativa",
            {"fields": ("project", "company", "product", "description",)},
        ),
    )

    class Meta:
        fields = "__all__"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("project", "company", "store", "product", "balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "store", "product")

    fieldsets = (
        ("Dados Cadastrais", {"fields": ("project", "company", "store", "product",)},),
        (
            "Quantidades",
            {"fields": ("owned", "sold", "sent", "received", "transit", "balance")},
        ),
    )

    class Meta:
        fields = "__all__"


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ("project", "company", "product", "balance", "syngenta_balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "product")

    fieldsets = (
        ("Dados Cadastrais", {"fields": ("project", "company", "product",)},),
        (
            "Quantidades",
            {
                "fields": (
                    "owned",
                    "sold",
                    "sent",
                    "received",
                    "transit",
                    "adjust",
                    "balance",
                )
            },
        ),
        (
            "Dados Syngenta",
            {"fields": ("syngenta_balance", "difference", "justification",)},
        ),
    )

    class Meta:
        fields = "__all__"
