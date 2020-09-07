from .models import Company, Store, Focal, CompanyFocal, Rtv, CompanyRtv
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


class CompanyFocalResource(resources.ModelResource):
    class Meta:
        model = CompanyFocal


class RtvResource(resources.ModelResource):
    class Meta:
        model = Rtv


class CompanyRtvResource(resources.ModelResource):
    class Meta:
        model = CompanyRtv
