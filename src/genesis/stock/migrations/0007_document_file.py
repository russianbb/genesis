# Generated by Django 2.2.16 on 2020-10-16 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0006_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="file",
            field=models.FileField(
                default=0, upload_to="stock/", verbose_name="Arquivo"
            ),
            preserve_default=False,
        ),
    ]
