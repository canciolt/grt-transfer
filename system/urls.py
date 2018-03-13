# -*- coding: utf-8 -*-
from django.conf.urls import url
from system.views import *
from system.ajax import *
from system.pdf import *

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
    url(r'^add/(?P<model>\w+)/(?P<pk>[\d+]+)$', Dinamic_Add.as_view(), name='add-consignatario'),
    url(r'^payments/$', PagosView.as_view(), name='payments'),
    # Ajax URL
    url(r'^ajax/cliente/estados/$', get_ciudades, name='ajax-estados'),
    url(r'^ajax/operacion/get_data_form/$', get_data_form, name='ajax-servicios'),
    url(r'^ajax/operacion/startop/$', startop, name='ajax-startop'),
    url(r'^ajax/operacion/change_sello/$', change_sello, name='ajax-change_sello'),
    url(r'^ajax/operacion/evento_add/$', event_add, name='ajax-event_add'),
    url(r'^ajax/operacion/concepto_add/$', concepto_add, name='ajax-concepto_add'),
    url(r'^ajax/operacion/delconcepop/$', delconcepop, name='ajax-concepto_delete'),
    url(r'^ajax/factura/get_client_operations/$', get_client_operations, name='ajax-client_operations'),
    url(r'^ajax/factura/reset_operations_json/$', reset_operations_json, name='ajax-reset-operations-json'),
    url(r'^ajax/factura/facturar/$', facturar, name='ajax-facturar'),
    url(r'^ajax/factura/cancel_factura/$', cancel_factura, name='ajax-cancel_factura'),
    url(r'^ajax/system/get_tasa_cambio/$', get_tasa, name='ajax-get-tasa'),
    url(r'^ajax/payments/payment/$', add_payment, name='ajax-add-payment'),
    url(r'^ajax/payments/checkmoney/$', checkmoney, name='ajax-checkmoney'),
    url(r'^ajax/payments/startpay/$', startpay, name='ajax-startpay'),
    url(r'^ajax/payments/get_payments_client/$', get_payments_client, name='ajax-get-payments-client'),
    url(r'^ajax/payments/report_main/$', report_main, name='ajax-payments-reportmain'),
    url(r'^ajax/camion/add_comb/$', add_comb, name='ajax-camion-add_comb'),
    url(r'^ajax/camion/add_comb_pista/$', add_comb_pista, name='ajax-camion-add_comb_pista'),

    # Generate pdf
#    url(r'^pdf/factura/get_factura/(?P<pk>[\d+]+)$', MyPDFView.as_view(), name='pdf-get-factura'),

]
