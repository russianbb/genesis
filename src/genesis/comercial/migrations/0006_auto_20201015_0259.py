# Generated by Django 2.2.16 on 2020-10-15 02:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comercial", "0005_auto_20201010_0426"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="designated",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="company",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Designado",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="focal",
            field=models.ManyToManyField(
                blank=True, related_name="company", to="comercial.Focal"
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="rtv",
            field=models.ManyToManyField(
                blank=True, related_name="company", to="comercial.Rtv"
            ),
        ),
    ]
