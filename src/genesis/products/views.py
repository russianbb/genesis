from comercial.models import Company
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from utils.views import StaffUserRequiredMixin

from .forms import CompanyProductForm
from .models import CompanyProduct, OnixProduct, SyngentaProduct


class OnixProductListView(StaffUserRequiredMixin, ListView):
    template_name = "products/onix/list.html"
    context_object_name = "products"
    model = OnixProduct


class OnixProductDetailView(StaffUserRequiredMixin, DetailView):
    template_name = "products/onix/detail.html"
    context_object_name = "product"
    model = OnixProduct

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("syngenta")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["syngenta"] = context["object"].syngenta.all()
        return context


class SyngentaProductListView(StaffUserRequiredMixin, ListView):
    template_name = "products/syngenta/list.html"
    context_object_name = "products"
    model = SyngentaProduct


class SyngentaProductDetailView(StaffUserRequiredMixin, DetailView):
    template_name = "products/syngenta/detail.html"
    context_object_name = "product"
    model = SyngentaProduct
    pk_url_kwarg = "agicode"


class CompanyProductFilterView(StaffUserRequiredMixin, ListView):
    template_name = "products/company/filter.html"
    context_object_name = "companies"
    model = Company


class CompanyProductListView(StaffUserRequiredMixin, ListView):
    template_name = "products/company/list.html"
    context_object_name = "products"
    model = CompanyProduct

    def get_queryset(self):
        queryset = super().get_queryset()
        code_sap = self.kwargs["code_sap"]
        return queryset.filter(company__code_sap=code_sap)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["code_sap"] = self.kwargs["code_sap"]
        return context


class CompanyProductDetailView(StaffUserRequiredMixin, DetailView):
    template_name = "products/company/detail.html"
    context_object_name = "product"
    model = CompanyProduct

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["code_sap"] = self.kwargs["code_sap"]
        return context


class CompanyProductEditView(StaffUserRequiredMixin, UpdateView):
    template_name = "products/company/create_edit.html"
    form_class = CompanyProductForm
    model = CompanyProduct

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["pk"]
        store = CompanyProduct.objects.get(pk=arg)
        store = model_to_dict(store)
        for key, value in store.items():
            initial[key] = value

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["code_sap"] = self.kwargs["code_sap"]
        context["title"] = "Editar Produto do Distribuidor"
        return context

    def get_success_url(self):
        code_sap = self.kwargs["code_sap"]
        return reverse_lazy("products:company_list", kwargs={"code_sap": code_sap})


class CompanyProductCreateView(StaffUserRequiredMixin, CreateView):
    template_name = "products/company/create_edit.html"
    form_class = CompanyProductForm
    model = CompanyProduct

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Responsável"
        context["code_sap"] = self.kwargs["code_sap"]
        return context

    def get_initial(self):
        initial = super().get_initial()
        arg = self.kwargs["code_sap"]
        company = Company.objects.filter(code_sap=arg).first()
        initial["company"] = company

        return initial

    def get_success_url(self):
        code_sap = self.kwargs["code_sap"]
        return reverse_lazy("products:company_list", kwargs={"code_sap": code_sap})
