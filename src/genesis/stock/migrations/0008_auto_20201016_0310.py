# Generated by Django 2.2.16 on 2020-10-16 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comercial", "0006_auto_20201015_0259"),
        ("stock", "0007_document_file"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="document",
            options={
                "ordering": ("date", "company", "category"),
                "verbose_name": "Documento",
                "verbose_name_plural": "Documentos",
            },
        ),
        migrations.AlterModelOptions(
            name="item",
            options={
                "ordering": ("date", "company", "product", "store"),
                "verbose_name": "Item",
                "verbose_name_plural": "Itens",
            },
        ),
        migrations.AddField(
            model_name="index",
            name="difference",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                max_digits=9,
                null=True,
                verbose_name="Divergência",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="document", unique_together={("date", "company", "category")},
        ),
    ]