from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("project", "company", "category", "file")
    list_display_links = ("file",)
    search_fields = ("project", "company", "category")

    fieldsets = (
        ("Documento", {"fields": ("project", "company", "category", "file",)},),
    )

    list_filter = ("project", "category")

    class Meta:
        fields = "__all__"
