from django.urls import path

from .views import CompanyViewSet, FocalViewSet, RtvViewSet

app_name = "comercial"

urlpatterns = [
    path("distribuidores/", CompanyViewSet.as_view(), name="company"),
    path("responsaveis/", FocalViewSet.as_view(), name="focal"),
    path("rtvs/", RtvViewSet.as_view(), name="rtv"),
]
