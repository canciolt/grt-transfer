# -*- coding: utf-8 -*-
from django.conf.urls import url
from system.views import *
from system.ajax import *


urlpatterns = [
   url(r'^$', IndexView.as_view(), name='home'),
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^logout/$', LogoutView.as_view(), name='logout'),
   url(r'^add/usuario/$', Registro_View.as_view(), name='add_user'),
   url(r'^update/passwd/(?P<pk>[\d+]+)$', Password_View.as_view(), name='update_passwd'),
   url(r'^add/(?P<model>\w+)/$', Dinamic_Add.as_view(), name='add'),
   url(r'^update/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Update.as_view(), name='update'),
   url(r'^list/(?P<model>\w+)/$', Dinamic_List.as_view(), name='list'),
   url(r'^delete/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Delete.as_view(), name='delete'),
   url(r'^detail/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Detail.as_view(), name='view'),
   url(r'^add/camion/(?P<model>\w+)/(?P<pk>[\d+]+)$', Add_Exta_Camion, name='add-camionextra'),

   # Ajax URL
   url(r'^ajax/cliente/estados/$', prueba, name='ajax-estados'),
]
