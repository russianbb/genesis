from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


def ping(request):
    return HttpResponse("pong")


@login_required
def index(request):
    return render(request, "index.html")
