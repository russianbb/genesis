# Generated by Django 2.2.19 on 2021-07-28 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comercial", "0002_auto_20201203_0120"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="store",
            options={
                "ordering": [
                    "status",
                    "company__trade_name",
                    "code",
                    "nickname",
                    "document",
                ],
                "verbose_name": "Filial",
                "verbose_name_plural": "Filiais",
            },
        ),
    ]
