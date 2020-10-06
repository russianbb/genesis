from .models import Company, Store, Focal, Rtv
from import_export import resources


# Models for Import-Export app
class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class StoreResource(resources.ModelResource):
    class Meta:
        model = Store


class FocalResource(resources.ModelResource):
    class Meta:
        model = Focal


class RtvResource(resources.ModelResource):
    class Meta:
        model = Rtv
