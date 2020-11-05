from django import forms
from django.utils.translation import ugettext_lazy
from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.forms import BRCNPJField, BRCPFField

from .models import Store

BRCPFField.default_error_messages = {
    "invalid": ugettext_lazy("Número do CPF inválido"),
    "max_digits": ugettext_lazy("Este campo requer 11 dígitos"),
}
BRCNPJField.default_error_messages = {
    "invalid": ugettext_lazy("Número do CNPJ inválido"),
    "max_digits": ugettext_lazy("Este campo requer 14 dígitos"),
}


class StoreForm(forms.ModelForm):
    document = BRCPFField(
        label="CPF do responsável",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "id_responsible_document"}
        ),
    )
    state = forms.ChoiceField(
        label="Estado",
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Store
        fields = "__all__"
        exclude = ("created_at", "updated_at")
        widgets = {
            "company": forms.TextInput(
                attrs={"class": "form-control", "disabled": True}
            ),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control"}),
            "ibge": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.TextInput(attrs={"class": "form-control"}),
        }
