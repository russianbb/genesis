from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = "projects/list.html"
    context_object_name = "projects"
    model = Project
