from django.db import models

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = AutoCreatedField(verbose_name="criado em")
    updated_at = AutoLastModifiedField(verbose_name="atualizado em")

    class Meta:
        abstract = True