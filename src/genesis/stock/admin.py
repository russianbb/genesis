from django.contrib import admin

from .models import Item, Index, CutDate, SyngentaBalance, Justification


@admin.register(CutDate)
class CutDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'description')
    list_display_links = list_display

    class Meta:
        fields = '__all__'


@admin.register(SyngentaBalance)
class SyngentaBalanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'company', 'product', 'balance')
    list_display_links = ('product', 'balance')
    search_fields = ('company', 'product', 'balance')

    class Meta:
        fields = '__all__'


@admin.register(Justification)
class JustificationAdmin(admin.ModelAdmin):
    list_display = ('date', 'company', 'product', 'description')
    list_display_links = ('description',)
    search_fields = ('company', 'product')

    class Meta:
        fields = '__all__'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('date', 'company', 'store', 'product', 'balance')
    list_display_links = ('product', 'balance')
    search_fields = ('company', 'store', 'product')

    class Meta:
        fields = '__all__'


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('date', 'company', 'product', 'balance', 'syngenta_balance')
    list_display_links = ('product', 'balance')
    search_fields = ('company', 'product')

    class Meta:
        fields = '__all__'