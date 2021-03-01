from django.conf import settings  # TODO: remover no deploy
from django.conf.urls.static import static  # TODO: remover no deploy
from django.contrib import admin
from django.urls import include, path

from .views import index, ping

urlpatterns = [
    path("", include("comercial.urls")),
    path("", include("finance.urls")),
    path("", include("products.urls")),
    path(r"", index, name="home"),
    path(r"ping/", ping),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # TODO: remover no deploy
