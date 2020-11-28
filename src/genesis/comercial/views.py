from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CompanyFocalForm, CompanyRtvForm, FocalForm, RtvForm, StoreForm
from .models import Company, CompanyFocal, CompanyRtv, Focal, Rtv, Store


class CompanyListView(LoginRequiredMixin, ListView):
    template_name = "comercial/company/list.html"
    context_object_name = "companies"
    model = Company


class CompanyDetailView(LoginRequiredMixin, DetailView):
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


class FocalListView(LoginRequiredMixin, ListView):
    template_name = "comercial/focal/list.html"
    context_object_name = "focals"
    model = Focal


class RtvListView(LoginRequiredMixin, ListView):
    template_name = "comercial/rtv/list.html"
    context_object_name = "rtvs"
    model = Rtv


class StoreDetailView(LoginRequiredMixin, DetailView):
    template_name = "comercial/store/detail.html"
    context_object_name = "store"
    model = Store

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company")


class StoreCreateView(LoginRequiredMixin, CreateView):
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


class StoreEditView(LoginRequiredMixin, UpdateView):
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


class FocalDetailView(LoginRequiredMixin, DetailView):
    template_name = "comercial/focal/detail.html"
    context_object_name = "focal"
    model = Focal


class FocalCreateView(LoginRequiredMixin, CreateView):
    template_name = "comercial/focal/create_edit.html"
    form_class = FocalForm
    model = Focal
    success_url = reverse_lazy("comercial:focals")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Responsável"
        return context


class FocalEditView(LoginRequiredMixin, UpdateView):
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


class RtvDetailView(LoginRequiredMixin, DetailView):
    template_name = "comercial/rtv/detail.html"
    context_object_name = "rtv"
    model = Rtv


class RtvCreateView(LoginRequiredMixin, CreateView):
    template_name = "comercial/rtv/create_edit.html"
    form_class = RtvForm
    model = Rtv
    success_url = reverse_lazy("comercial:rtvs")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Adicionar Responsável"
        return context


class RtvEditView(LoginRequiredMixin, UpdateView):
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


class CompanyFocalCreateView(LoginRequiredMixin, CreateView):
    template_name = "comercial/company/assign.html"
    model = CompanyFocal
    form_class = CompanyFocalForm
    success_url = "/distribuidores/{company_id}/"

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["company"]
        company = Company.objects.get(pk=arg)
        initial["company"] = company
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Atribuir Responsável"
        context["label"] = "Responsável"
        return context


class CompanyFocalDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "comercial/company/unassign.html"
    model = CompanyFocal
    success_url = "/distribuidores/{company_id}/"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company", "focal")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        company = self.kwargs["company"]
        focal = self.kwargs["focal"]

        queryset = CompanyFocal.objects.filter(company=company, focal=focal)

        if not queryset:
            raise Http404

        context = {"company_id": company, "focal_id": focal}
        return context

    def delete(self, request, *args, **kwargs):
        company = self.kwargs["company"]
        focal = self.kwargs["focal"]

        unassign = CompanyFocal.objects.filter(company=company, focal=focal)
        unassign.delete()

        return HttpResponseRedirect(
            reverse("comercial:company", kwargs={"pk": company})
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        company = Company.objects.get(pk=self.kwargs["company"])
        focal = Focal.objects.get(pk=self.kwargs["focal"])

        context["title"] = "Desatribuir Responsável"
        context["label"] = "Responsável"
        context["focal"] = focal
        context["company"] = company
        return context


class CompanyRtvCreateView(LoginRequiredMixin, CreateView):
    template_name = "comercial/company/assign.html"
    model = CompanyRtv
    form_class = CompanyRtvForm
    success_url = "/distribuidores/{company_id}/"

    def get_initial(self):
        initial = super().get_initial()

        arg = self.kwargs["company"]
        company = Company.objects.get(pk=arg)
        initial["company"] = company
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Atribuir RTV"
        context["label"] = "RTV"
        return context


class CompanyRtvDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "comercial/company/unassign.html"
    model = CompanyRtv
    success_url = "/distribuidores/{company_id}/"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("company", "rtv")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        company = self.kwargs["company"]
        rtv = self.kwargs["rtv"]

        queryset = CompanyRtv.objects.filter(company=company, rtv=rtv)

        if not queryset:
            raise Http404

        context = {"company_id": company, "rtv_id": rtv}
        return context

    def delete(self, request, *args, **kwargs):
        company = self.kwargs["company"]
        rtv = self.kwargs["rtv"]

        unassign = CompanyRtv.objects.filter(company=company, rtv=rtv)
        unassign.delete()

        return HttpResponseRedirect(
            reverse("comercial:company", kwargs={"pk": company})
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        company = Company.objects.get(pk=self.kwargs["company"])
        rtv = Rtv.objects.get(pk=self.kwargs["rtv"])

        context["title"] = "Desatribuir RTV"
        context["label"] = "RTV"
        context["rtv"] = rtv
        context["company"] = company
        return context
