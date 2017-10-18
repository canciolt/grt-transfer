# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin
from django.views.generic import RedirectView
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from system.models import *
from system.views import get_tasa_cambio
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from system.forms import Sellos_Form, Evento_Form
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import json
import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404


@login_required
@ajax
def get_ciudades(request):
    if request.method == 'POST':
        r = request.POST['pais']
        filePath = os.path.join(settings.BASE_DIR, 'system\json\ciudades.json')
        ciudades = json.load(open(filePath))
        choice = []
        for c in ciudades:
            if c['value'] == request.POST['pais']:
                choice.append((c['value'], c['pais']))
        return choice
    raise Http404

@login_required
@ajax
def get_data_form(request):
    if request.method == 'POST':
        client = request.POST['cliente']
        choice = dict()
        extra = []
        cruce = []
        consig = []
        caja = []
        if client != '':
            servicios = Servicio.objects.filter(cliente=client)
            for c in servicios:
                try:
                    service = Servicio_Cruce.objects.get(pk=c.id)
                    cruce.append((service.id, service.get_tipo_display()))
                except:
                    service = Servicio_Extra.objects.get(pk=c.id)
                    extra.append((service.id, service.get_tipo_display()))
            consignatarios = Consignatario.objects.filter(cliente=client, usuario__is_active=True)
            for c in consignatarios:
                consig.append((c.id, c.usuario.first_name))
            cajas = Caja.objects.filter(cliente=client, estado=False, fecha_entrada__lte=datetime.now(),
                                        fecha_salida__gt=datetime.now())
            for c in cajas:
                caja.append((c.id, c.numero))
            choice['cruce'] = cruce
            choice['extra'] = extra
            choice['consig'] = consig
            choice['caja'] = caja
        return choice
    raise Http404


@login_required
@ajax
@csrf_protect
def facturar(request):
    if request.method == 'POST':
        client = request.POST['cliente']
        op = request.POST.get('operaciones')
        op_list = json.loads(op)
        operaciones = []
        cliente = get_object_or_404(Cliente, pk=int(client))
        for o in op_list:
            temp_op = get_object_or_404(Operacion, pk=int(o))
            conc_operacion = Concepto_Operacion.objects.filter(operacion=temp_op.id)
            imp_usd = temp_op.servicio.importeusd
            imp_mxn = temp_op.servicio.importemx
            for conc in conc_operacion:
                imp_usd += conc.cantidad * conc.costo_usd
                imp_mxn += conc.cantidad * conc.costo_mx
            if temp_op.servicio.iva == True:
                imp_usd += imp_usd * 0.16
                imp_mxn += imp_mxn * 0.16
            operaciones.append({"id": temp_op.id, "fecha": temp_op.fecha, "servicio": temp_op.servicio, \
                                "consignatario": temp_op.consignatario, "importeusd": imp_usd, "importemxn": imp_mxn})
        filePath = os.path.join(settings.BASE_DIR, "system/templates/prefactura_form.html")
        if 'approved' in request.POST:
            pass
        else:
            context = {'cliente': cliente, "operaciones": operaciones}
            return render(request, filePath, context)
    else:
        raise Http404


@login_required
@ajax
def get_client_operations(request):
    if request.method == 'POST':
        client = request.POST['cliente']
        choice = dict()
        opera = []
        filePath = os.path.join(settings.BASE_DIR, 'static\system\json\operaciones.json')
        jsonFile = open(filePath, "w+")
        if client != '':
            operaciones = Operacion.objects.filter(cliente=client, facturada=False, estado="T")
            for o in operaciones:
                opera.append({"#": str(o.id), "fecha": o.fecha.strftime('%m/%d/%Y'), "cliente": str(o.cliente), \
                              "operador": str(o.operador), "servicio": str(o.servicio), \
                              "opciones": " <div class='checkbox checkbox-success'><input id='checkbox-" + str(
                                  o.id) + "' type='checkbox'><label for='checkbox-" + str(
                                  o.id) + "'> Facturar </label></div>"})
            choice['data'] = opera
            jsonFile.write(json.dumps(choice))
            jsonFile.close()
        else:
            choice['data'] = []
            jsonFile.write(json.dumps(choice))
            jsonFile.close()
        return True
    raise Http404


@login_required
@ajax
def reset_operations_json(request):
    if request.method == 'POST':
        choice = dict()
        filePath = os.path.join(settings.BASE_DIR, 'static\system\json\operaciones.json')
        jsonFile = open(filePath, "w+")
        choice['data'] = []
        jsonFile.write(json.dumps(choice))
        jsonFile.close()
        return True
    raise Http404


@login_required
@ajax
def startop(request):
    if request.method == 'POST':
        try:
            op = Operacion.objects.get(id=request.POST['operacion'])
            if op.estado == "P":
                op.estado = "I"
                op.save()
                return True
            messages.add_message(request, messages.ERROR, 'Error al cambiar de estado. Contacte el Administrador !')
            return False
        except:
            messages.add_message(request, messages.ERROR, 'Error al cambiar de estado. Contacte el Administrador !')
            return False
    raise Http404


@login_required
@ajax
def get_tasa(request):
    if request.method == 'POST':
        tasa = get_tasa_cambio(request)
        return tasa
    raise Http404

@login_required
@ajax
@csrf_protect
def change_sello(request):
    if request.method == 'POST':
        form = Sellos_Form(data=request.POST)
        context = {'form_sello': form}
        filePath = os.path.join(settings.BASE_DIR, "system/templates/sellos_form.html")
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Sello agregado satisfactoriamente')
            return 1
        else:
            return render(request, filePath, context)
    raise Http404


@login_required
@ajax
@csrf_protect
def event_add(request):
    if request.method == 'POST':
        form = Evento_Form(data=request.POST)
        context = {'form_evento': form}
        filePath = os.path.join(settings.BASE_DIR, "system/templates/evento_form.html")
        if form.is_valid():
            form.save()
            if request.POST['evento'] == "CAN":
                operacion = get_object_or_404(Operacion, pk=request.POST['operacion'])
                operacion.estado = "C"
                operacion.save()
                ope = get_object_or_404(Operador, pk=operacion.operador.id)
                ope.estado = False
                ope.save()
                ca = get_object_or_404(Caja, pk=operacion.caja.id)
                ca.estado = False
                ca.save()
            if request.POST['evento'] == "FIN":
                operacion = get_object_or_404(Operacion, pk=request.POST['operacion'])
                operacion.estado = "T"
                operacion.save()
                ope = get_object_or_404(Operador, pk=operacion.operador.id)
                ope.estado = False
                ope.save()
                ca = get_object_or_404(Caja, pk=operacion.caja.id)
                ca.estado = False
                ca.save()
            messages.add_message(request, messages.SUCCESS, 'Evento agregado satisfactoriamente')
            return 1
        else:
            return render(request, filePath, context)
    raise Http404


@method_decorator(login_required, name='dispatch')
class LogoutView(AJAXMixin, RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)