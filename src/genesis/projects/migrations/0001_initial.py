# Generated by Django 2.2.19 on 2021-07-28 02:26

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("comercial", "0003_auto_20210728_0132"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                    "category",
                    models.CharField(
                        choices=[
                            ("circularizacao", "Circularização de Estoque"),
                            ("inventario", "Inventário Físico"),
                        ],
                        max_length=200,
                        verbose_name="Tipo de projeto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Projeto",
                "verbose_name_plural": "Projetos",
                "ordering": ("-date",),
            },
        ),
        migrations.CreateModel(
            name="ProjectCompany",
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
                        to="comercial.Company",
                        verbose_name="Distribuidor",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.Project",
                        verbose_name="Projeto",
                    ),
                ),
            ],
            options={
                "verbose_name": "distribuidor do drojeto",
                "verbose_name_plural": "distribuidores do drojeto",
                "ordering": ("-project", "company__trade_name"),
                "unique_together": {("project", "company")},
            },
        ),
        migrations.AddField(
            model_name="project",
            name="companies",
            field=models.ManyToManyField(
                related_name="projects",
                through="projects.ProjectCompany",
                to="comercial.Company",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="project", unique_together={("date", "category")},
        ),
    ]
