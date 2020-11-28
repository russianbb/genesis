from django.contrib import admin
from django.urls import include, path

from .views import index, ping

urlpatterns = [
    path("", include("comercial.urls")),
    path("", include("products.urls")),
    path(r"", index, name="home"),
    path(r"ping/", ping),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]
