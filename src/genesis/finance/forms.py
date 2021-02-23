from decimal import Decimal

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Category, CostCenter, Invoice, Transaction


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["category"].queryset = Category.objects.filter(cash_flow="expense")
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)


class InvoicePayForm(forms.ModelForm):
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
        self.fields["document"].widget.attrs = {"class": "form-control"}
        self.fields["amount"].widget.attrs = {"class": "form-control"}
        self.fields["transacted_at"].widget.attrs = {"class": "form-control"}

    def clean_amount(self):
        invoice_amount = Decimal(self.initial["amount"])
        form_amount = Decimal(self.data["amount"])
        if form_amount > invoice_amount:
            raise ValidationError("O valor recebido é maior que o permitido")
        return self.data["amount"]


def get_dividends_receiver_choices():
    superusers = User.objects.filter(is_superuser=True).all()
    receiver_choices = []
    for _ in superusers:
        receiver_choices.append((_.username, _.get_full_name))
    return receiver_choices


class DividendsPayForm(forms.ModelForm):

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
        self.fields["document"].widget.attrs = {"class": "form-control"}
        self.fields["amount"].widget.attrs = {"class": "form-control"}
        self.fields["transacted_at"].widget.attrs = {"class": "form-control"}
        self.fields["receiver"].widget.attrs = {"class": "form-control"}
        self.fields["cost_center"].queryset = CostCenter.objects.filter(status=True)
