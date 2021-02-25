# Generated by Django 2.2.16 on 2021-02-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_auto_20210220_0415"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="category",
            field=models.CharField(
                choices=[("invoice", "Nota Fiscal"), ("debit", "Nota de Débito")],
                max_length=20,
                verbose_name="Categoria",
            ),
        ),
    ]