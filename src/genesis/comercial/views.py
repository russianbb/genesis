from django.views.generic import CreateView, DetailView, ListView

from .forms import StoreForm
from .models import Company, Focal, Rtv, Store


class CompanyListView(ListView):
    template_name = "comercial/company/list.html"
    context_object_name = "companies"
    model = Company


class CompanyDetailView(DetailView):
    template_name = "comercial/company/detail.html"
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


class StoreDetailView(DetailView):
    template_name = "comercial/store/detail.html"
    context_object_name = "store"
    model = Store

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company")


class StoreCreateView(CreateView):
    template_name = "comercial/store/create_edit.html"
    form_class = StoreForm
    model = Store
    success_url = "/distribuidores/{company_id}/"

    def get_initial(self):
        arg = self.kwargs["company"]
        company = Company.objects.get(pk=arg)

        initial = super().get_initial()
        initial["company"] = company

        return initial
