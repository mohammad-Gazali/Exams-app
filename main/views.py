from django.shortcuts import render
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def index(request: HttpRequest):
    return render(request, 'index.html')