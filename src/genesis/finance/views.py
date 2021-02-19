from django.contrib import messages
from django.views.generic import CreateView
from utils.views import SuperUserRequiredMixin

from .forms import ExpenseForm
from .models import Transaction


class ExpenseCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "finance/expense/create_edit.html"
    form_class = ExpenseForm
    model = Transaction
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Despesa cadastrada com sucesso!")
        return super().form_valid(form)


expense_create = ExpenseCreateView.as_view()
