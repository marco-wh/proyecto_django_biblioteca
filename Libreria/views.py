from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import Template, Context, loader
from django import forms

import datetime

def index(request):
    return render(request, 'index.html')

def hola(request):
    return HttpResponse("Hola Mundo")

def fecha_actual(request):
    ahora = datetime.datetime.now()
    return render(request, 'fecha_actual.html', {'fecha_actual': ahora})

def horas_adelante(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404

    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)

    return render(request, 'horas_adelante.html', {'hora_siguiente': dt, 'horas': offset})

def atributos_meta(request):
    valor = request.META.items()

    return render(request, 'atributos_meta.html', {'meta': valor})