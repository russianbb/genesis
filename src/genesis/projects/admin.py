from django.contrib import admin

from .models import Project, ProjectCompany, ProjectCompanyDocument
from .tasks import send_project_initial_email, send_project_initial_email_custom_cutoff


def send_initial_email(self, request, queryset):
    for project_company in queryset:
        send_project_initial_email.apply_async(
            kwargs={
                "project_id": project_company.project.id,
                "company_id": project_company.company.id,
            }
        )


send_initial_email.short_description = (
    "Enviar e-mail inicial: solicitação de relatórios"
)


def send_initial_email_custom_cutoff(self, request, queryset):
    for project_company in queryset:
        send_project_initial_email_custom_cutoff.apply_async(
            kwargs={"project_company_id": project_company.id}
        )


send_initial_email_custom_cutoff.short_description = (
    "Enviar e-mail inicial com data customizada: solicitação de relatórios"
)


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

    fieldsets = (
        (
            "Projeto",
            {
                "fields": (
                    "date",
                    "category",
                    "status",
                )
            },
        ),
    )

    inlines = (ProjectCompanyInline,)

    class Meta:
        fields = "__all__"


@admin.register(ProjectCompany)
class ProjectCompanyAdmin(admin.ModelAdmin):
    list_display = ("project", "company")
    list_filter = ("project",)
    search_fields = (
        "project__date",
        "project__category",
        "company__company_name",
        "company__trade_name",
        "company__code_sap",
    )

    actions = [send_initial_email, send_initial_email_custom_cutoff]


@admin.register(ProjectCompanyDocument)
class ProjectCompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "project", "company", "description")
    list_filter = ("project",)
    search_fields = (
        "project__date",
        "project__category",
        "company__company_name",
        "company__trade_name",
        "company__code_sap",
        "description",
    )
