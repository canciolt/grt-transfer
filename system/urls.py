# -*- coding: utf-8 -*-
from django.conf.urls import url
from system.views import *


urlpatterns = [

   url(r'^$', IndexView.as_view(), name='home'),
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^logout/$', LogoutView.as_view(), name='logout'),
   url(r'^add/(?P<model>\w+)/$', Dinamic_Add.as_view(), name='add'),
   url(r'^update/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Update.as_view(), name='update'),
   url(r'^list/(?P<model>\w+)/$', Dinamic_List.as_view(), name='list'),
   url(r'^delete/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Delete.as_view(), name='delete'),
   url(r'^detail/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Detail.as_view(), name='view'),
   url(r'^add/camion/(?P<model>\w+)/(?P<pk>[\d+]+)$', Add_Exta_Camion, name='add-camionextra'),
]
