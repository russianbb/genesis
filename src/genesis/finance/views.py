from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from utils.constants import TRANSACTION_CATEGORY_DIVIDENDS
from utils.views import SuperUserRequiredMixin

from .forms import (
    BillForm,
    DividendsPayForm,
    ExpenseForm,
    ReceivableForm,
    ReceivableReceiveForm,
)
from .functions import (
    get_active_cost_center,
    get_balance_until,
    get_billings_history,
    get_bills_not_paid,
    get_cost_center_chart_data,
    get_receivables_not_received_data,
    process_statement_report,
)
from .models import Bill, Expense, Receivable, Transaction, TransactionCategory


class DashboardView(SuperUserRequiredMixin, TemplateView):
    template_name = "finance/dashboard.html"

    def get_context_data(self, **kwargs):
        context = {}

        context["statementreportstart"] = (
            datetime.now() - relativedelta(months=1)
        ).strftime("%d-%m-%Y")
        context["statementreportend"] = datetime.now().strftime("%d-%m-%Y")

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

        context["bills_not_paid"] = get_bills_not_paid

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
                transacted_at__gte=self.start_date,
                transacted_at__lte=self.end_date,
                is_paid=True,
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
    template_name = "finance/expense/create.html"
    form_class = ExpenseForm
    model = Expense
    success_url = reverse_lazy("finance:dashboard")

    def get_initial(self):
        return {"transacted_at": datetime.now().strftime("%d-%m-%Y")}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.set_as_paid

        if self.object.is_recurrent:
            self.object.create_recurrent
            messages.success(
                self.request, "Agendamento de pagamento cadastrado com sucesso!"
            )
        messages.success(self.request, "Pagamento cadastrado com sucesso!")

        return super().form_valid(form)


class BillPayView(SuperUserRequiredMixin, UpdateView):
    template_name = "finance/bill/pay.html"
    form_class = ExpenseForm
    model = Bill
    success_url = reverse_lazy("finance:dashboard")

    def get_initial(self):
        return {
            "transacted_at": datetime.now().strftime("%d-%m-%Y"),
            "is_recurrent": "checked" if self.object.is_recurrent else None,
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = True
        self.object.save()
        self.object.set_as_paid

        if self.object.is_recurrent:
            self.object.create_recurrent
            messages.success(
                self.request, "Agendamento de pagamento cadastrado com sucesso!"
            )
        messages.success(self.request, "Pagamento cadastrado com sucesso!")

        return super().form_valid(form)


class BillCreateView(SuperUserRequiredMixin, UpdateView):
    template_name = "finance/bill/create_edit.html"
    form_class = BillForm
    model = Bill
    success_url = reverse_lazy("finance:dashboard")

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            initial["is_recurrent"] = "checked" if self.object.is_recurrent else None
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = True
        self.object.save()

        messages.success(
            self.request, "Agendamento de pagamento cadastrado com sucesso!"
        )

        return super().form_valid(form)


class ReceivableCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/create.html"
    form_class = ReceivableForm
    model = Receivable
    success_url = reverse_lazy("finance:dashboard")

    def get_initial(self):
        return {"issued_at": datetime.now().strftime("%d-%m-%Y"), "is_recurrent": False}

    def form_valid(self, form):
        messages.success(self.request, "Recebível cadastrado com sucesso!")
        return super().form_valid(form)


class ReceivableListView(SuperUserRequiredMixin, ListView):
    template_name = "finance/receivable/list.html"
    context_object_name = "receivables"
    model = Receivable


class ReceivableReceiveView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/receive.html"
    model = Transaction
    form_class = ReceivableReceiveForm
    success_url = reverse_lazy("finance:dashboard")

    def get_initial(self):
        number = self.kwargs["number"]
        self.receivable = Receivable.objects.filter(number=number).first()
        transaction_category = TransactionCategory.objects.filter(
            description=self.receivable.get_transaction_category
        ).first()
        if not self.receivable:
            raise Http404
        return {
            "transacted_at": datetime.now().strftime("%d-%m-%Y"),
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
        transaction = form.save(commit=False)
        transaction.set_as_paid
        self.object = transaction.save()

        self.receivable.set_as_received

        messages.success(self.request, "Recebimento cadastrado com sucesso!")
        return super().form_valid(form)


class DividendsPayView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/receivable/dividends_pay.html"
    model = Transaction
    form_class = DividendsPayForm
    success_url = reverse_lazy("finance:dashboard")

    def get_initial(self):
        number = self.kwargs["number"]
        self.receivable = Receivable.objects.filter(number=number).first()
        transaction_category = TransactionCategory.objects.filter(
            description=TRANSACTION_CATEGORY_DIVIDENDS["description"]
        ).first()
        if not self.receivable:
            raise Http404
        return {
            "transacted_at": datetime.now().strftime("%d-%m-%Y"),
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
        transaction.set_as_paid
        self.object = transaction.save()
        messages.success(self.request, "Pagamento de dividendo cadastrado com sucesso!")
        return super().form_valid(form)


bill_create_edit = BillCreateView.as_view()
bill_pay = BillPayView.as_view()
dashboard = DashboardView.as_view()
dividends_pay = DividendsPayView.as_view()
expense_create = ExpenseCreateView.as_view()
receivable_create = ReceivableCreateView.as_view()
receivable_list = ReceivableListView.as_view()
receivable_receive = ReceivableReceiveView.as_view()
statement_report = StatementReportView.as_view()
