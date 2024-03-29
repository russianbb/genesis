# Generated by Django 2.2.19 on 2022-05-03 04:47

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import utils.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Atualizado em",
                    ),
                ),
                ("status", models.BooleanField(default=True, verbose_name="Ativo")),
                (
                    "description",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Descrição"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[("syngenta", "Syngenta")],
                        max_length=255,
                        verbose_name="Categoria",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=utils.models.UploadTo("documents/"),
                        verbose_name="Arquivo",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Enviado Por",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
