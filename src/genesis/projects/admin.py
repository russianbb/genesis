from django.contrib import admin

from .models import Project, ProjectCompany


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("date", "category")
    list_display_links = list_display
    list_filter = ("date", "category")
    search_fields = list_display

    fieldsets = (("Data Base", {"fields": ("date", "category", "status",)},),)

    class Meta:
        fields = "__all__"


@admin.register(ProjectCompany)
class ProjectCompanyAdmin(admin.ModelAdmin):
    list_display = ("project", "company")
    list_display_links = list_display
    list_filter = ("project",)
    search_fields = list_display

    fieldsets = (("Participante", {"fields": ("project", "company",)},),)

    class Meta:
        fields = "__all__"
