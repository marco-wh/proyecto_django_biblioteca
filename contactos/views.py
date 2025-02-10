from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import *

def contactos(request):
    if request.method == 'POST':
        form = FormContactos(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/contactos/gracias')
    else:
        form = FormContactos(initial={'asunto': "¡Adoro tu sitio!"})

    return render(request, 'form_contactos.html', {'form': form})

def gracias(request):
    return HttpResponse("<h1>Gracias por tu mensaje</h1>")
