from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from .views import index, ping

urlpatterns = [
    path("", include("comercial.urls")),
    path(r"", index),
    path(r"ping/", ping),
    path("admin/", admin.site.urls),
    path(r"logout", LogoutView.as_view(), name="logout"),
    path(r"login", LoginView.as_view(), name="login"),
]
