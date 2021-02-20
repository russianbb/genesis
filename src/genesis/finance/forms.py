from django import forms

from .models import Category, Invoice, Transaction


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


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}


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
