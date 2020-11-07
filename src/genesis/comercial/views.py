from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import FocalForm, RtvForm, StoreForm
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
    template_name = "comercial/focal/list.html"
    context_object_name = "focals"
    model = Focal


class RtvListView(ListView):
    template_name = "comercial/rtv/list.html"
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
        initial = super().get_initial()

        arg = self.kwargs["company"]
        company = Company.objects.get(pk=arg)
        initial["company"] = company

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Filial"
        return context


class StoreEditView(UpdateView):
    template_name = "comercial/store/create_edit.html"
    form_class = StoreForm
    model = Store
    success_url = "/distribuidores/{company_id}/"

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["pk"]
        store = Store.objects.get(pk=arg)
        store = model_to_dict(store)
        for key, value in store.items():
            initial[key] = value

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Editar Filial"
        return context


class FocalDetailView(DetailView):
    template_name = "comercial/focal/detail.html"
    context_object_name = "focal"
    model = Focal


class FocalCreateView(CreateView):
    template_name = "comercial/focal/create_edit.html"
    form_class = FocalForm
    model = Focal
    success_url = reverse_lazy("comercial:focals")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Responsável"
        return context


class FocalEditView(UpdateView):
    template_name = "comercial/focal/create_edit.html"
    form_class = FocalForm
    model = Focal
    success_url = reverse_lazy("comercial:focals")

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["pk"]
        focal = Focal.objects.get(pk=arg)
        focal = model_to_dict(focal)
        for key, value in focal.items():
            initial[key] = value
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Editar Responsável"
        return context


class RtvDetailView(DetailView):
    template_name = "comercial/rtv/detail.html"
    context_object_name = "rtv"
    model = Rtv


class RtvCreateView(CreateView):
    template_name = "comercial/rtv/create_edit.html"
    form_class = RtvForm
    model = Rtv
    success_url = reverse_lazy("comercial:rtvs")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Responsável"
        return context


class RtvEditView(UpdateView):
    template_name = "comercial/rtv/create_edit.html"
    form_class = RtvForm
    model = Rtv
    success_url = reverse_lazy("comercial:rtvs")

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["pk"]
        rtv = Rtv.objects.get(pk=arg)
        rtv = model_to_dict(rtv)
        for key, value in rtv.items():
            initial[key] = value
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Editar Responsável"
        return context
