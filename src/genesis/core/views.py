from django.http import HttpResponse
from django.shortcuts import render


def ping(request):
    return HttpResponse("pong")

def index(request):
    return render(request, 'index.html')