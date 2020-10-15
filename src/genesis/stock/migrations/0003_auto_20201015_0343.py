# Generated by Django 2.2.16 on 2020-10-15 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201008_0044'),
        ('comercial', '0006_auto_20201015_0259'),
        ('stock', '0002_auto_20201015_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='index',
            name='adjust',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True, verbose_name='Ajuste'),
        ),
        migrations.AddField(
            model_name='index',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque calculado. Saldo = EF - VEF + Em Terceiros - De Terceiros +- Transito +- Ajuste', max_digits=9, null=True, verbose_name='Saldo Calculado'),
        ),
        migrations.AddField(
            model_name='index',
            name='owned',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico', max_digits=9, null=True, verbose_name='EF'),
        ),
        migrations.AddField(
            model_name='index',
            name='received',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico de terceiros armazenado em poder do distribuidor (Remessa recebida)', max_digits=9, null=True, verbose_name='De Terceiros'),
        ),
        migrations.AddField(
            model_name='index',
            name='sent',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico do distribuidor armazenado em poder de terceiros (Remessa para enviada)', max_digits=9, null=True, verbose_name='Em Terceiros'),
        ),
        migrations.AddField(
            model_name='index',
            name='sold',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de venda para entrega futura faturada com CFOP 5922, 6922', max_digits=9, null=True, verbose_name='VEF'),
        ),
        migrations.AddField(
            model_name='index',
            name='transit',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico em trânsito', max_digits=9, null=True, verbose_name='Em Trânsito'),
        ),
        migrations.AddField(
            model_name='item',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque calculado. Saldo = EF - VEF + Em Terceiros - De Terceiros +- Transito', max_digits=9, null=True, verbose_name='Saldo Calculado'),
        ),
        migrations.AddField(
            model_name='item',
            name='owned',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico', max_digits=9, null=True, verbose_name='EF'),
        ),
        migrations.AddField(
            model_name='item',
            name='received',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico de terceiros armazenado em poder do distribuidor (Remessa recebida)', max_digits=9, null=True, verbose_name='De Terceiros'),
        ),
        migrations.AddField(
            model_name='item',
            name='sent',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico do distribuidor armazenado em poder de terceiros (Remessa para enviada)', max_digits=9, null=True, verbose_name='Em Terceiros'),
        ),
        migrations.AddField(
            model_name='item',
            name='sold',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de venda para entrega futura faturada com CFOP 5922, 6922', max_digits=9, null=True, verbose_name='VEF'),
        ),
        migrations.AddField(
            model_name='item',
            name='transit',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque físico em trânsito', max_digits=9, null=True, verbose_name='Em Trânsito'),
        ),
        migrations.AlterField(
            model_name='syngentabalance',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Saldo de estoque informado pela Syngenta. (Posição Sales Force)', max_digits=9, null=True, verbose_name='Saldo Syngenta'),
        ),
        migrations.AlterUniqueTogether(
            name='syngentabalance',
            unique_together={('date', 'company', 'product', 'balance')},
        ),
    ]
