from django.conf import settings
from django.db import models
from model_utils.choices import Choices
from utils.models import AbstractBaseModel, UploadTo


class Document(AbstractBaseModel):
    UPLOAD_PATH = "documents/"
    DOCUMENT_CATEGORY = Choices(("syngenta", "Syngenta"))

    description = models.CharField(
        max_length=200, unique=True, verbose_name="Descrição"
    )
    category = models.CharField(
        choices=DOCUMENT_CATEGORY, max_length=255, verbose_name="Categoria",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Enviado Por",
        related_name="document",
    )
    file = models.FileField(
        upload_to=UploadTo(base_path=UPLOAD_PATH), verbose_name="Arquivo",
    )

    def __str__(self):
        return f"{self.file}"
