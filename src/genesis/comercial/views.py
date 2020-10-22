from django.views.generic import ListView

from .models import Company, Focal, Rtv


class CompanyViewSet(ListView):
    template_name = "comercial/company.html"
    context_object_name = "companies"
    model = Company


class FocalViewSet(ListView):
    template_name = "comercial/focal.html"
    context_object_name = "focals"
    model = Focal


class RtvViewSet(ListView):
    template_name = "comercial/rtv.html"
    context_object_name = "rtvs"
    model = Rtv
