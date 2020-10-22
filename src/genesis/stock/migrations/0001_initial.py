# Generated by Django 2.2.16 on 2020-10-15 02:59

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0002_auto_20201008_0044"),
        ("comercial", "0006_auto_20201015_0259"),
    ]

    operations = [
        migrations.CreateModel(
            name="CutDate",
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
                    "date",
                    models.DateField(
                        help_text="Data de mensuração do estoque",
                        verbose_name="Data Base",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Nome do projeto ou descrição do momento em que se mensura os estoques",
                        max_length=200,
                        verbose_name="Descrição",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="SyngentaBalance",
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
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="syngenta_balance",
                        to="comercial.Company",
                        verbose_name="Distribuidor",
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="syngenta_balance",
                        to="stock.CutDate",
                        verbose_name="Data Base",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="syngenta_balance",
                        to="products.OnixProduct",
                        verbose_name="Produto Onix",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Justification",
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
                ("description", models.TextField(verbose_name="Justificativa")),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="justification",
                        to="comercial.Company",
                        verbose_name="Distribuidor",
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="justification",
                        to="stock.CutDate",
                        verbose_name="Data Base",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="justification",
                        to="products.OnixProduct",
                        verbose_name="Produto Onix",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Item",
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
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item",
                        to="comercial.Company",
                        verbose_name="Distribuidor",
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item",
                        to="stock.CutDate",
                        verbose_name="Data Base",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item",
                        to="products.OnixProduct",
                        verbose_name="Produto Onix",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item",
                        to="comercial.Store",
                        verbose_name="Filial",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Index",
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
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="index",
                        to="comercial.Company",
                        verbose_name="Distribuidor",
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="index",
                        to="stock.CutDate",
                        verbose_name="Data Base",
                    ),
                ),
                (
                    "justification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="index",
                        to="stock.Justification",
                        verbose_name="Justificativa",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="index",
                        to="products.OnixProduct",
                        verbose_name="Produto Onix",
                    ),
                ),
                (
                    "syngenta_balance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="index",
                        to="stock.SyngentaBalance",
                        verbose_name="Saldo Syngenta",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]