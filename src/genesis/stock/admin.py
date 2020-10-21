from django.contrib import admin

from .models import CutDate, Document, Index, Item, Justification, SyngentaBalance


@admin.register(CutDate)
class CutDateAdmin(admin.ModelAdmin):
    list_display = ("date", "description")
    list_display_links = list_display

    fieldsets = (("Data Base", {"fields": ("date", "description", "status",)},),)

    class Meta:
        fields = "__all__"


@admin.register(SyngentaBalance)
class SyngentaBalanceAdmin(admin.ModelAdmin):
    list_display = ("date", "company", "product", "balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "product", "balance")

    fieldsets = (
        ("Saldo Syngenta", {"fields": ("date", "company", "product", "balance",)},),
    )

    class Meta:
        fields = "__all__"


@admin.register(Justification)
class JustificationAdmin(admin.ModelAdmin):
    list_display = ("date", "company", "product", "description")
    list_display_links = ("description",)
    search_fields = ("company", "product")

    fieldsets = (
        ("Justificativa", {"fields": ("date", "company", "product", "description",)},),
    )

    class Meta:
        fields = "__all__"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("date", "company", "store", "product", "balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "store", "product")

    fieldsets = (
        ("Dados Cadastrais", {"fields": ("date", "company", "store", "product",)},),
        (
            "Quantidades",
            {"fields": ("owned", "sold", "sent", "received", "transit", "balance")},
        ),
    )

    class Meta:
        fields = "__all__"


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ("date", "company", "product", "balance", "syngenta_balance")
    list_display_links = ("product", "balance")
    search_fields = ("company", "product")

    fieldsets = (
        ("Dados Cadastrais", {"fields": ("date", "company", "product",)},),
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


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("date", "company", "category", "file")
    list_display_links = ("file",)
    search_fields = ("date", "company", "category")

    fieldsets = (("Documentos", {"fields": ("date", "company", "category", "file",)},),)

    list_filter = ("date", "category")

    class Meta:
        fields = "__all__"
