from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import Http404
from django.views.generic import CreateView, ListView, TemplateView
from utils.constants import CATEGORY_DIVIDENDS
from utils.views import SuperUserRequiredMixin

from .forms import DividendsPayForm, ExpenseForm, ReceivableForm, ReceivableReceiveForm
from .functions import (
    get_active_cost_center,
    get_balance_until,
    get_billings_history,
    get_cost_center_chart_data,
    get_receivables_not_received_data,
    process_statement_report,
)
from .models import Category, Receivable, Transaction


class DashboardView(SuperUserRequiredMixin, TemplateView):
    template_name = "finance/dashboard.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["balance"] = get_balance_until()

        receivables_data = get_receivables_not_received_data()
        context["receivables_not_received"] = receivables_data[
            "receivables_not_received"
        ]
        context["amount_not_received"] = receivables_data["amount_not_received"]

        billings_data = get_billings_history()
        context["billings_12_months"] = billings_data["billings_12_months"]
        context["billings_annual"] = billings_data["billings_annual"]

        context["cost_centers_active"] = get_active_cost_center()

        context["cost_center_chart"] = get_cost_center_chart_data()

        return context


class StatementReportView(SuperUserRequiredMixin, ListView):
    template_name = "finance/statement/report.html"
    context_object_name = "transactions"
    model = Transaction

    def get_queryset(self):
        queryset = super().get_queryset()

        params = self.request.GET

        self.start_date = datetime.now() - relativedelta(days=1, months=1)
        if params.get("start"):
            self.start_date = datetime.strptime(params["start"], ("%d-%m-%Y"))

        self.end_date = datetime.now()
        if params.get("end"):
            self.end_date = datetime.strptime(params["end"], ("%d-%m-%Y"))

        return (
            queryset.filter(
                transacted_at__gte=self.start_date, transacted_at__lte=self.end_date
            )
            .select_related("category")
            .order_by("transacted_at",)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_date"] = self.start_date
        context["end_date"] = self.end_date
        context["start_balance"] = get_balance_until(self.start_date)
        context["reports"] = process_statement_report(context)
        return context


class ExpenseCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/expense/create_edit.html"
    form_class = ExpenseForm
    model = Transaction
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Despesa cadastrada com sucesso!")
        return super().form_valid(form)


class ReceivableCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/create_edit.html"
    form_class = ReceivableForm
    model = Receivable
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Recebível cadastrado com sucesso!")
        return super().form_valid(form)


class ReceivableListView(SuperUserRequiredMixin, ListView):
    template_name = "finance/receivable/list.html"
    context_object_name = "receivables"
    model = Receivable


class ReceivableReceiveView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/pay.html"
    model = Transaction
    form_class = ReceivableReceiveForm
    success_url = "/"  # TODO: redirecionar para a página do centro de custo

    def get_initial(self):
        number = self.kwargs["number"]
        self.receivable = Receivable.objects.filter(number=number).first()
        transaction_category = Category.objects.filter(
            description=self.receivable.get_transaction_category
        ).first()
        if not self.receivable:
            raise Http404
        return {
            "transacted_at": datetime.now(),
            "amount": self.receivable.amount,
            "cost_center": self.receivable.cost_center,
            "category": transaction_category,
            "notes": f"{transaction_category} - {self.receivable.number}",  # noqa
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receivable"] = self.receivable
        return context

    def form_valid(self, form):
        self.receivable.set_received
        messages.success(self.request, "Recebimento cadastrado com sucesso!")
        return super().form_valid(form)


class DividendsPayView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/dividends_pay.html"
    model = Transaction
    form_class = DividendsPayForm
    success_url = "/"  # TODO: redirecionar para a página do centro de custo

    def get_initial(self):
        number = self.kwargs["number"]
        self.receivable = Receivable.objects.filter(number=number).first()
        transaction_category = Category.objects.filter(
            description=CATEGORY_DIVIDENDS["description"]
        ).first()
        if not self.receivable:
            raise Http404
        return {
            "transacted_at": datetime.now(),
            "cost_center": self.receivable.cost_center,
            "category": transaction_category,
            "notes": f"Pagamento de Dividendos | {self.receivable.get_category_display()} - {self.receivable.number}",  # noqa
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receivable"] = self.receivable
        return context

    def form_valid(self, form):
        notes = f"{self.receivable.get_category_display()} {self.receivable.number} | {form.cleaned_data['receiver']}"  # noqa
        transaction = form.save(commit=False)
        transaction.notes = notes
        self.object = transaction.save()
        messages.success(self.request, "Pagamento de dividendo cadastrado com sucesso!")
        return super().form_valid(form)


dashboard = DashboardView.as_view()
dividends_pay = DividendsPayView.as_view()
expense_create = ExpenseCreateView.as_view()
receivable_create = ReceivableCreateView.as_view()
receivable_list = ReceivableListView.as_view()
receivable_receive = ReceivableReceiveView.as_view()
statement_report = StatementReportView.as_view()
