from django.views.generic import DetailView, ListView
from utils.views import LoginRequiredMixin, StaffUserRequiredMixin

from .models import Project, ProjectCompanyDocument


class ProjectListView(StaffUserRequiredMixin, ListView):
    template_name = "projects/list.html"
    context_object_name = "projects"
    model = Project


class ProjectDetailView(StaffUserRequiredMixin, DetailView):
    template_name = "projects/detail.html"
    model = Project

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("companies")


class ProjectCompanyDocumentList(LoginRequiredMixin, ListView):
    template_name = "projects/documents.html"
    model = ProjectCompanyDocument
    success_url = "/"
    context_object_name = "project_documents"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(project__status=True)
        return queryset.prefetch_related("company", "project")
