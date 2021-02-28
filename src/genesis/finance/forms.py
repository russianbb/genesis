from decimal import Decimal

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Category, CostCenter, Receivable, Transaction


class ExpenseForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", required=True)
    bill_id = forms.IntegerField(label="Conta a Pagar", required=False)

    class Meta:
        model = Transaction
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["bill_id"].widget = forms.HiddenInput()
        self.fields["category"].queryset = Category.objects.filter(cash_flow="expense")
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


def get_dividends_receiver_choices():
    superusers = User.objects.filter(is_superuser=True).all()
    receiver_choices = []
    for _ in superusers:
        receiver_choices.append((_.username, _.get_full_name))
    return receiver_choices


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
