from django.urls import path

from .views import upload

app_name = "documents"

urlpatterns = [
    path("upload/", upload, name="create"),
]
