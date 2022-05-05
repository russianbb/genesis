from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = ("description", "category", "sender", "file", "created_at")
    fields = ("description", "category", "sender", "file", "created_at")
    search_fields = ("description", "category", "sender", "file")
