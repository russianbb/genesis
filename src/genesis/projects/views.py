from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    template_name = "projects/list.html"
    context_object_name = "projects"
    model = Project

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=True)


class ProjectDetailView(DetailView):
    pass
