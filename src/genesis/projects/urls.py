from django.urls import path

from .views import ProjectDetailView, ProjectListView

app_name = "projects"

urlpatterns = [
    path("projetos/", ProjectListView.as_view(), name="list"),
    path("projetos/<int:pk>", ProjectDetailView.as_view(), name="detail"),
]
