from django.shortcuts import render
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from .forms import SendingEmailForm



def index(request: HttpRequest):
    return render(request, 'index.html')


def about_us(request: HttpRequest):
    return render(request, 'about_us.html')


def contact(request: HttpRequest):

    #? ---------------------------------
    #TODO: Add The Sending Functionality
    #? ---------------------------------

    form = SendingEmailForm()
    return render(request, 'contact.html', {"form": form})


def support(request: HttpRequest):
    return render(request, 'support.html')