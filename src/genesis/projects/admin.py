from django.contrib import admin

from .models import Project, ProjectCompany


class ProjectCompanyInline(admin.TabularInline):
    model = ProjectCompany
    raw_id_fields = ("company",)
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("date", "category")
    list_display_links = list_display
    list_filter = ("date", "category")
    search_fields = list_display

    fieldsets = (("Projeto", {"fields": ("date", "category", "status",)},),)

    inlines = (ProjectCompanyInline,)

    class Meta:
        fields = "__all__"


@admin.register(ProjectCompany)
class ProjectCompanyAdmin(admin.ModelAdmin):
    list_display = ("project", "company")
    list_filter = ("project",)
    search_fields = ("project", "company")
