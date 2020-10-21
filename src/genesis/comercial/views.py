from django.views.generic import ListView, TemplateView

from .models import Company, Focal, Rtv, Store


class CompanyViewSet(ListView):
    template_name = "comercial/company.html"
    context_object_name = "companies"
    model = Company


class FocalViewSet(TemplateView):
    template_name = "comercial/focal.html"


class RtvViewSet(TemplateView):
    template_name = "comercial/rtv.html"
