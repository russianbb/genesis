from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .functions import get_dividends_receiver_choices
from .models import (
    Bill,
    CostCenter,
    Expense,
    Receivable,
    Transaction,
    TransactionCategory,
)


class ExpenseForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    is_recurrent = forms.BooleanField(label="Agendar Próxima?", required=False)
    transacted_at = forms.DateField(label="Data de Transação", required=True)
    due_date = forms.DateField(label="Data de Vencimento", required=False)

    class Meta:
        model = Expense
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["category"].queryset = TransactionCategory.objects.filter(
            cash_flow="expense"
        )
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)
        self.fields["due_date"].widget = forms.HiddenInput()

    def clean_amount(self):
        return self.data["amount"].replace(",", ".")


class BillForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    # is_recurrent = forms.BooleanField(label="Agendar Próxima?", required=False)
    transacted_at = forms.DateField(label="Data de Transação", required=False)
    due_date = forms.DateField(label="Data de Vencimento")

    class Meta:
        model = Bill
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["category"].queryset = TransactionCategory.objects.filter(
            cash_flow="expense"
        )
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)

    def clean_amount(self):
        return self.data["amount"].replace(",", ".")


class ReceivableForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    taxes = forms.CharField(label="Impostos", required=True)

    class Meta:
        model = Receivable
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)

    def clean_amount(self):
        return self.data["amount"].replace(",", ".")

    def clean_taxes(self):
        return self.data["taxes"].replace(",", ".")


class ReceivableReceiveForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    transacted_at = forms.DateField(label="Data da Transação", required=True)

    class Meta:
        model = Transaction
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                "class": "form-control",
                "readonly": True,
            }
        self.fields["file"].widget.attrs = {"class": "form-control"}
        self.fields["amount"].widget.attrs = {"class": "form-control"}
        self.fields["transacted_at"].widget.attrs = {"class": "form-control"}

    def clean_amount(self):
        receivable_amount = Decimal(self.initial["amount"])
        form_amount = Decimal(self.data["amount"].replace(",", "."))
        if form_amount > receivable_amount:
            raise ValidationError("O valor recebido é maior que o permitido")
        return form_amount


class DividendsPayForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    receiver = forms.ChoiceField(
        choices=get_dividends_receiver_choices(), label="Pago para"
    )

    class Meta:
        model = Transaction
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                "class": "form-control",
                "readonly": True,
            }
        self.fields["file"].widget.attrs = {"class": "form-control"}
        self.fields["amount"].widget.attrs = {"class": "form-control"}
        self.fields["transacted_at"].widget.attrs = {"class": "form-control"}
        self.fields["receiver"].widget.attrs = {"class": "form-control"}
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)

    def clean_amount(self):
        return self.data["amount"].replace(",", ".")
