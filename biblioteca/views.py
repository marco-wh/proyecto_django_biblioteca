from urllib import request

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import LibroForm, AutorForm, EditorForm
from .models import *
import os

def form_buscar(request):
    return render(request, 'form_buscar.html')

def buscar(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append("Introduce un término de búsqueda")
        elif len(q)>20:
            errors.append("Introduce un término de búsqueda menor a 20 caracteres")
        else:
            libros = Libro.objects.filter(titulo__icontains=q)
            return render(request, 'resultados.html', {'libros': libros, 'query': q})

    return render(request, 'form_buscar.html', {'errors': errors})

def ver_libro(request, id):
    libro = Libro.objects.filter(id=id)
    if libro:
        context = {'object': libro[0]}
    else:
        messages.error(request, 'Libro no encontrado')
        return redirect('listar_libro')

    return render(request, 'ver_libro.html', context)

def listar_libro(request):
    libros = Libro.objects.all()
    context = {'libros': libros}
    return render(request, 'listar_libro.html', context)

def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro registrado correctamente')
            return redirect('listar_libro')
        else:
            messages.error(request, 'Error al registrar. Corrige los datos y vuelve a intentarlo.')
    else:
        form = LibroForm()

    return render(request, 'registrar_libro.html', {'form': form})

def editar_libro(request, id):
    libro = Libro.objects.filter(id=id)
    if not libro:
        messages.error(request, 'Libro no encontrado')
        return redirect('listar_libro')

    libro = libro[0]
    ruta = libro.portada.path

    if request.method == 'GET':
        form = LibroForm(instance=libro)
    else:
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            if 'portada' in form.files:
                if os.path.exists(ruta):
                    os.remove(ruta)

            form.save()
            messages.success(request, 'Libro actualizado correctamente')
            return redirect('listar_libro')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')

    return render(request, 'editar_libro.html', {'form': form})

def eliminar_libro(request, id):
    libro = Libro.objects.filter(id=id)
    if not libro:
        messages.error(request, 'Libro no encontrado')
        return redirect('listar_libro')

    libro = libro[0]
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente')
        return redirect('listar_libro')

    return render(request, 'eliminar_libro.html', {'libro': libro})

class LibroListView(ListView):
    model = Libro
    template_name = 'listar_libro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libros'] = context['object_list']
        del context['object_list']
        return context

class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'registrar_libro.html'
    success_url = reverse_lazy('listar_class_libro')

    def form_valid(self, form):
        messages.success(self.request, 'Libro actualizado correctamente')
        return super(LibroCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')
        return super(LibroCreateView, self).form_invalid(form)

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'ver_libro.html'

    def get_object(self, queryset=None):
        libro = self.model.objects.filter(id=self.kwargs['pk'])
        if libro:
            return libro[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Libro no encontrado.')
            return redirect('listar_libro')
        else:
            return super(LibroDetailView, self).dispatch(request, *args, **kwargs)

class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'editar_libro.html'

    def get_object(self, queryset=None):
        libro = self.model.objects.filter(id=self.kwargs['pk'])
        if libro:
            return libro[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Libro no encontrado.')
            return redirect('listar_libro')
        else:
            return super(LibroUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        libro = self.model.objects.get(id=self.kwargs['pk'])
        form = LibroForm(request.POST, request.FILES, instance=libro)
        ruta = libro.portada.path

        if form.is_valid():
            if 'portada' in form.files:
                if os.path.exists(ruta):
                    os.remove(ruta)

            form.save()
            messages.success(request, 'Libro actualizado correctamente')
            return redirect('listar_class_libro')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')

        return render(request, 'editar_libro.html', {'form': form})

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'eliminar_libro.html'
    success_url = reverse_lazy('listar_libro')

    def get_object(self, queryset=None):
        libro = self.model.objects.filter(id=self.kwargs['pk'])
        if libro:
            return libro[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Libro no encontrado')
            return redirect('listar_libro')
        else:
            return super(LibroDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        libro = self.get_object()
        ruta = libro.portada.path
        response = super(LibroDeleteView, self).delete(request, *args, **kwargs)
        if os.path.exists(ruta):
            os.remove(ruta)

        messages.success(request, 'Libro eliminado correctamente')
        return response

def ver_autor(request, id):
    autor = Autor.objects.filter(id=id)
    if autor:
        autor = autor[0]
    else:
        messages.error(request, 'Autor no encontrado.')
        return redirect('listar_autor')

    return render(request, 'ver_autor.html', {'autor': autor})

def listar_autor(request):
    autores = Autor.objects.all()
    context = {'autores': autores}
    return render(request, 'listar_autor.html', context)

def registrar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor registrado correctamente')
            return redirect('listar_autor')
        else:
            messages.error(request, 'Error al registrar. Corrige los datos y vuelve a intentarlo.')
    else:
        form = AutorForm()

    return render(request, 'registrar_autor.html', {'form': form})

def editar_autor(request, id):
    autor = Autor.objects.filter(id=id)
    if autor:
        autor = autor[0]
    else:
        messages.error(request, 'Autor no encontrado.')
        return redirect('listar_autor')

    if request.method == 'GET':
        form = AutorForm(instance=autor)
    else:
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor actualizado correctamente')
            return redirect('listar_autor')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')
    return render(request, 'editar_autor.html', {'form': form })

def eliminar_autor(request, id):
    autor = Autor.objects.filter(id=id)
    if autor:
        autor = autor[0]
    else:
        messages.error(request, 'Autor no encontrado.')
        return redirect('listar_autor')

    if request.method == 'GET':
        form = AutorForm(instance=autor)
    else:
        autor.delete()
        messages.success(request, 'Autor eliminado correctamente')
        return redirect('listar_autor')

    return render(request, 'eliminar_autor.html', {'autor': autor })

class AutorListView(ListView):
    model = Autor
    template_name = 'listar_autor.html'
    context_object_name = 'autores'

class AutorDetailView(DetailView):
    model = Autor
    template_name = 'ver_autor.html'
    context_object_name = 'autor'

    def get_object(self, queryset=None):
        autor = self.model.objects.filter(id=self.kwargs['pk'])
        if autor:
            return autor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Autor no encontrado')
            return redirect('listar_class_autor')
        else:
            return super(AutorDetailView, self).dispatch(request, *args, **kwargs)

class AutorCreateView(CreateView):
    model = Autor
    template_name = 'registrar_autor.html'
    form_class = AutorForm
    success_url = reverse_lazy('listar_class_autor')

    def form_valid(self, form):
        messages.success(self.request, 'Autor creado correctamente')
        return super(AutorCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al registrar. Corrige los datos y vuelve a intentarlo.')
        return super(AutorCreateView, self).form_invalid(form)

class AutorUpdateView(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'editar_autor.html'
    success_url = reverse_lazy('listar_class_autor')


    def get_object(self, queryset=None):
        autor = self.model.objects.filter(pk=self.kwargs['pk'])
        if autor:
            return autor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Autor no encontrado.')
            return redirect('listar_class_autor')
        else:
            return super(AutorUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Autor actualizado correctamente')
        return super(AutorUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')
        return super(AutorUpdateView, self).form_invalid(form)

class AutorDeleteView(DeleteView):
    model = Autor
    form_class = AutorForm
    template_name = 'eliminar_autor.html'
    success_url = reverse_lazy('listar_class_autor')

    def get_object(self, queryset=None):
        autor = self.model.objects.filter(pk=self.kwargs['pk'])
        if autor:
            return autor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Autor no encontrado.')
            return redirect('listar_class_autor')
        else:
            return super(AutorDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Autor eliminado correctamente')
        return super(AutorDeleteView, self).delete(request, *args, **kwargs)

def ver_editor(request, id):
    editor = Editor.objects.filter(id=id)
    if editor:
        editor = editor[0]
    else:
        messages.error(request, 'Editor no encontrado.')
        return redirect('listar_editor')

    return render(request, "ver_editor.html", {'editor': editor})

def listar_editor(request):
    editores = Editor.objects.all()
    context = {'editores': editores}
    return render(request, 'listar_editor.html', context)

def registrar_editor(request):
    if request.method == 'POST':
        form = EditorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editor registrado correctamente')
            return redirect('listar_editor')
        else:
            messages.error(request, 'Error al registrar. Corrige los datos y vuelve a intentarlo.')
    else:
        form = EditorForm()
    return render(request, 'registrar_editor.html', {'form': form})

def editar_editor(request, id):
    editor = Editor.objects.filter(id=id)
    if editor:
        editor = editor[0]
    else:
        messages.error(request, 'Editor no encontrado.')
        return redirect('listar_editor')

    if request.method == 'POST':
        form = EditorForm(request.POST, instance=editor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editor actualizado correctamente')
            return redirect('listar_editor')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')
    else:
        form = EditorForm(instance=editor)

    return render(request, 'editar_editor.html', {'form': form})

def eliminar_editor(request, id):
    editor = Editor.objects.filter(id=id)
    if editor:
        editor = editor[0]
    else:
        messages.error(request, 'Editor no encontrado.')
        return redirect('listar_editor')

    if request.method == 'POST':
        editor.delete()
        messages.success(request, 'Editor eliminado correctamente')
        return redirect('listar_editor')
    else:
        context = {'editor': editor}

    return render(request, 'eliminar_editor.html', context)

class EditorDetailView(DetailView):
    model = Editor
    template_name = 'ver_editor.html'
    context_object_name = 'editor'

    def get_object(self, queryset=None):
        editor = self.model.objects.filter(pk=self.kwargs['pk'])
        if editor:
            return editor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Editor no encontrado.')
            return redirect('listar_editor')
        else:
            return super(EditorDetailView, self).dispatch(request, *args, **kwargs)

class EditorListView(ListView):
    model = Editor
    template_name = 'listar_editor.html'
    context_object_name = 'editores'

class EditorCreateView(CreateView):
    model = Editor
    form_class = EditorForm
    template_name = 'registrar_editor.html'
    success_url = reverse_lazy('listar_editor')

    def form_valid(self, form):
        messages.success(self.request, 'Editor registrado correctamente')
        return super(EditorCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al registrar. Corrige los datos y vuelve a intentarlo.')
        return super(EditorCreateView, self).form_invalid(form)

class EditorUpdateView(UpdateView):
    model = Editor
    form_class = EditorForm
    template_name = 'editar_editor.html'
    success_url = reverse_lazy('listar_editor')

    def get_object(self, queryset=None):
        editor = self.model.objects.filter(pk=self.kwargs['pk'])
        if editor:
            return editor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Editor no encontrado.')
            return redirect('listar_editor')
        else:
            return super(EditorUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Editor actualizado correctamente')
        return super(EditorUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar. Corrige los datos y vuelve a intentarlo.')
        return super(EditorUpdateView, self).form_invalid(form)

class EditorDeleteView(DeleteView):
    model = Editor
    template_name = 'eliminar_editor.html'
    success_url = reverse_lazy('listar_editor')
    context_object_name = 'editor'

    def get_object(self, queryset=None):
        editor = self.model.objects.filter(pk=self.kwargs['pk'])
        if editor:
            return editor[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'Editor no encontrado.')
            return redirect('listar_editor')
        else:
            return super(EditorDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Editor eliminado correctamente')
        return super(EditorDeleteView, self).delete(request, *args, **kwargs)