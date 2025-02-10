from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^form_buscar/$', form_buscar, name='form_buscar'),
    url(r'^buscar/$', buscar, name='buscar'),

    url(r'^libro/view/ver/(?P<id>\d+)/$', ver_libro, name='ver_libro'),
    url(r'libro/view/registrar/$', registrar_libro, name='registrar_libro'),
    url(r'^libro/view/lista/$', listar_libro, name='listar_libro'),
    url(r'^libro/view/editar/(?P<id>\d+)/$', editar_libro, name='editar_libro'),
    url(r'^libro/view/eliminar/(?P<id>\d+)/$', eliminar_libro, name='eliminar_libro'),

    url(r'libro/class/registrar/$', LibroCreateView.as_view(), name='registrar_class_libro'),
    url(r'^libro/class/ver/(?P<pk>\d+)/$', LibroDetailView.as_view(), name='ver_class_libro'),
    url(r'^libro/class/lista/$', LibroListView.as_view(), name='listar_class_libro'),
    url(r'^libro/class/editar/(?P<pk>\d+)/$', LibroUpdateView.as_view(), name='editar_class_libro'),
    url(r'^libro/class/eliminar/(?P<pk>\d+)/$', LibroDeleteView.as_view(), name='eliminar_class_libro'),

    url(r'^autor/view/ver/(?P<id>\d+)/$', ver_autor, name='ver_autor'),
    url(r'^autor/view/lista/$', listar_autor, name='listar_autor'),
    url(r'^autor/view/registrar/$', registrar_autor, name='registrar_autor'),
    url(r'^autor/view/editar/(?P<id>\d+)/$', editar_autor, name='editar_autor'),
    url(r'^autor/view/eliminar/(?P<id>\d+)/$', eliminar_autor, name='eliminar_autor'),

    url(r'^autor/class/ver/(?P<pk>\d+)/$', AutorDetailView.as_view(), name='ver_class_autor'),
    url(r'^autor/class/lista/$', AutorListView.as_view(), name='listar_class_autor'),
    url(r'^autor/class/registrar/$', AutorCreateView.as_view(), name='registrar_class_autor'),
    url(r'^autor/class/editar/(?P<pk>\d+)/$', AutorUpdateView.as_view(), name='editar_class_autor'),
    url(r'^autor/class/eliminar/(?P<pk>\d+)/$', AutorDeleteView.as_view(), name='eliminar_class_autor'),

    url (r'^editor/view/lista/$', listar_editor, name='listar_editor'),
    url(r'^editor/view/ver/(?P<id>\d+)/$', ver_editor, name='ver_editor'),
    url(r'^editor/view/registrar/$', registrar_editor, name='registrar_editor'),
    url(r'^editor/view/editar/(?P<id>\d+)/$', editar_editor, name='editar_editor'),
    url(r'^editor/view/eliminar/(?P<id>\d+)/$', eliminar_editor, name='eliminar_editor'),

    url(r'^editor/class/ver/(?P<pk>\d+)/$', EditorDetailView.as_view(), name='ver_class_editor'),
    url(r'^editor/class/lista/$', EditorListView.as_view(), name='listar_class_editor'),
    url(r'^editor/class/registrar/$', EditorCreateView.as_view(), name='registrar_class_editor'),
    url(r'^editor/class/editar/(?P<pk>\d+)/$', EditorUpdateView.as_view(), name='editar_class_editor'),
    url(r'^editor/class/eliminar/(?P<pk>\d+)/$', EditorDeleteView.as_view(), name='eliminar_class_editor'),

]

