from datetime import datetime

from django.contrib import messages
from django.http import Http404
from django.views.generic import CreateView, ListView
from utils.views import SuperUserRequiredMixin

from .forms import ExpenseForm, InvoiceForm, InvoicePayForm
from .models import Category, Invoice, Transaction


class ExpenseCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/expense/create_edit.html"
    form_class = ExpenseForm
    model = Transaction
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Despesa cadastrada com sucesso!")
        return super().form_valid(form)


class InvoiceCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/invoice/create_edit.html"
    form_class = InvoiceForm
    model = Invoice
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Recebível cadastrado com sucesso!")
        return super().form_valid(form)


class InvoiceListView(SuperUserRequiredMixin, ListView):
    template_name = "finance/invoice/list.html"
    context_object_name = "invoices"
    model = Invoice


class InvoicePayView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/invoice/pay.html"
    model = Transaction
    form_class = InvoicePayForm
    success_url = "/"  # TODO: redirecionar para a página do centro de custo

    def get_initial(self):
        number = self.kwargs["number"]
        self.invoice = Invoice.objects.filter(number=number).first()
        transaction_category = Category.objects.filter(
            description=self.invoice.get_transaction_category
        ).first()
        if not self.invoice:
            raise Http404
        return {
            "transacted_at": datetime.now(),
            "amount": self.invoice.amount,
            "cost_center": self.invoice.cost_center,
            "category": transaction_category,
            "notes": f"Pagamento {self.invoice.get_category_display()} - {self.invoice.number}",  # noqa
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invoice"] = self.invoice
        return context


expense_create = ExpenseCreateView.as_view()
invoice_create = InvoiceCreateView.as_view()
invoice_list = InvoiceListView.as_view()
invoice_pay = InvoicePayView.as_view()
