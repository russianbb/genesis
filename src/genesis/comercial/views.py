from django.views.generic import DetailView, ListView

from .models import Company, Focal, Rtv


class CompanyListView(ListView):
    template_name = "comercial/companies.html"
    context_object_name = "companies"
    model = Company


class CompanyDetailView(DetailView):
    template_name = "comercial/company.html"
    context_object_name = "company"
    model = Company

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("designated").prefetch_related(
            "stores", "rtv", "focal"
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rtvs"] = context["object"].rtv.all()
        context["focals"] = context["object"].focal.all()
        context["stores"] = context["object"].stores.all()
        return context


class FocalListView(ListView):
    template_name = "comercial/focals.html"
    context_object_name = "focals"
    model = Focal


class RtvListView(ListView):
    template_name = "comercial/rtvs.html"
    context_object_name = "rtvs"
    model = Rtv
