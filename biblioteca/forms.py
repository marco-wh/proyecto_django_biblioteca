from django import forms
from .models import *
from django.contrib.admin.widgets import AdminFileWidget


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autores', 'editor', 'fecha_publicacion', 'portada']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'editor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control'}),
            'portada': AdminFileWidget(attrs={'class': 'form-control'}),
        }

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ['nombre', 'domicilio', 'ciudad', 'estado', 'pais', 'website']

    nombre = forms.CharField(max_length=30)
    domicilio = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    estado = forms.CharField(max_length=30)
    pais = forms.CharField(max_length=50)
    website = forms.URLField()

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellidos', 'email']

    nombre = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=40)
    email = forms.EmailField()