# Generated by Django 2.2.16 on 2021-02-20 04:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["description"],
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
            },
        ),
        migrations.AlterModelOptions(
            name="costcenter",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Centro de Custo",
                "verbose_name_plural": "Centros de Custos",
            },
        ),
        migrations.AlterModelOptions(
            name="invoice",
            options={
                "ordering": ["-issued_at", "-number"],
                "verbose_name": "Recebível",
                "verbose_name_plural": "Recebíveis",
            },
        ),
        migrations.AlterModelOptions(
            name="serviceorder",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Ordem de Serviço",
                "verbose_name_plural": "Ordens de Serviço",
            },
        ),
        migrations.AlterModelOptions(
            name="transaction",
            options={
                "ordering": ["-transacted_at", "-id"],
                "verbose_name": "Transação",
                "verbose_name_plural": "Transações",
            },
        ),
        migrations.AlterField(
            model_name="transaction",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="finance.Category",
                verbose_name="Categoria",
            ),
        ),
    ]