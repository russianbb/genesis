from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = ("description", "category", "sender", "file")
    fields = ("description", "category", "sender", "file")
    search_fields = ("description", "category", "sender", "file")
