from django.views.generic import DetailView, ListView

from .models import CompanyProduct, OnixProduct, SyngentaProduct


class OnixProductListView(ListView):
    template_name = "products/onix/list.html"
    context_object_name = "products"
    model = OnixProduct


class OnixProductDetailView(DetailView):
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


class SyngentaProductListView(ListView):
    template_name = "products/syngenta/list.html"
    context_object_name = "products"
    model = SyngentaProduct


class SyngentaProductDetailView(DetailView):
    template_name = "products/syngenta/detail.html"
    context_object_name = "product"
    model = SyngentaProduct
    pk_url_kwarg = "agicode"


class CompanyProductListView(ListView):
    template_name = "products/company/list.html"
    context_object_name = "products"
    model = CompanyProduct


class CompanyProductDetailView(DetailView):
    template_name = "products/company/detail.html"
    context_object_name = "product"
    model = CompanyProduct
