from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .forms import DocumentForm
from .models import Document


class DocumentUploadView(LoginRequiredMixin, CreateView):
    template_name = "documents/create.html"
    form_class = DocumentForm
    model = Document
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()

        messages.success(self.request, "Documento enviado com sucesso!")

        return super().form_valid(form)


upload = DocumentUploadView.as_view()
