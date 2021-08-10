from django.urls import path

from .views import ProjectListView

app_name = "projects"

urlpatterns = [
    path("projetos/", ProjectListView.as_view(), name="list"),
]
