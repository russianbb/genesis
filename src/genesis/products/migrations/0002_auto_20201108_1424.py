# Generated by Django 2.2.16 on 2020-11-08 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="syngentaproduct",
            name="onix",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="syngenta",
                to="products.OnixProduct",
                verbose_name="Produto Onix",
            ),
        ),
    ]
