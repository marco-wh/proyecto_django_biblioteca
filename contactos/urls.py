from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', contactos, name='contactos'),
    url(r'^gracias/$', gracias, name='gracias'),
]