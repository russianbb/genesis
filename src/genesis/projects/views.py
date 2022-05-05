from django.views.generic import DetailView, ListView
from utils.views import StaffUserRequiredMixin

from .models import Project


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
