from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = "projects/list.html"
    context_object_name = "projects"
    model = Project


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = "projects/detail.html"
    model = Project

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("companies")
