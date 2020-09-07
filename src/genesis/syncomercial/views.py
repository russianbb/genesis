from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Company
# Create your views here.

# class CompanyView(ListView):
#    model = Company
#    template_name = 'syncomercial/base.html'