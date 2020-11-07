from django import forms
from localflavor.br.br_states import STATE_CHOICES

from .models import Focal, Store


class StoreForm(forms.ModelForm):
    state = forms.ChoiceField(label="Estado", choices=STATE_CHOICES,)

    class Meta:
        model = Store
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["company"].widget.attrs = {"class": "form-control"}
        self.fields["inventory"].widget.attrs = {"class": "form-control"}


class FocalForm(forms.ModelForm):
    class Meta:
        model = Focal
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
