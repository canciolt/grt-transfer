# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin
from django.views.generic import RedirectView
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from system.models import *
from system.views import get_tasa_cambio
from datetime import datetime, timedelta
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from system.forms import Sellos_Form, Evento_Form, Concepto_Form
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
        if 'cajaop' in request.POST:
            cajaop = request.POST['cajaop']
        else:
            cajaop = 0
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
                    cruce.append((service.id, service))
                except:
                    service = Servicio_Extra.objects.get(pk=c.id)
                    extra.append((service.id, service))
            consignatarios = Consignatario.objects.filter(cliente=client, usuario__is_active=True)
            for c in consignatarios:
                consig.append((c.id, c.usuario.first_name))
            if cajaop != 0:
                cajas = (Caja.objects.filter(pk=cajaop, cliente=client) | Caja.objects.filter(cliente=client, estado=False, fecha_entrada__lte=datetime.now(),
                                            fecha_salida__gt=datetime.now())).distinct()
            else:
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
        iva = 0
        subtotalmx = 0
        subtotalusd = 0
        totalmx = 0
        totalusd = 0
        for o in op_list:
            temp_op = get_object_or_404(Operacion, pk=int(o))
            conc_operacion = Concepto_Operacion.objects.filter(operacion=temp_op.id).order_by('fecha_concepto')
            imp_usd = temp_op.servicio.importeusd
            imp_mxn = temp_op.servicio.importemx
            subtotalmx += imp_mxn
            subtotalusd += imp_usd
            if temp_op.servicio.iva == True:
                iva += imp_mxn * 0.16
            for conc in conc_operacion:
                subtotalusd += conc.costo_usd
                subtotalmx += conc.costo_mx
                if temp_op.servicio.iva == True:
                    iva += conc.costo_mx * 0.16
            operaciones.append({"id": temp_op.id, "fecha": temp_op.fecha_inicio, "servicio": temp_op.servicio, \
                                "consignatario": temp_op.consignatario, "importeusd": imp_usd, "importemxn": imp_mxn,
                                "conceptos": conc_operacion})
        totalmx += subtotalmx + iva
        totalusd += subtotalusd
        if 'approved' in request.POST:
            cadena = str(timezone.now().year) + "-" + str(cliente.id)
            nfac = Factura.objects.filter(nfactura__contains=cadena).count()
            nfactura = cadena + '-' + str(nfac + 1).zfill(4)
            expira = timezone.now() + timedelta(days=cliente.facturacion)
            tasa = get_tasa_cambio(request)['tasa']
            tasa = 0
            try:
                if 'is_fmxn' in request.POST and request.POST['is_fmxn'] == 'true':
                    tasa = get_tasa_cambio(request)['tasa']
                    mx = totalmx + totalusd * float(tasa)
                    fact = Factura.objects.create(nfactura=nfactura, cliente=cliente, expira=expira, total_usd=0, \
                                                  total_mx=mx, tasa_cambio=tasa)
                else:
                    fact = Factura.objects.create(nfactura=nfactura, cliente=cliente, expira=expira, total_usd=totalusd, \
                                                  total_mx=totalmx, tasa_cambio=tasa)
                for op in op_list:
                    opera = get_object_or_404(Operacion, pk=int(op))
                    fact_op = Factura_Operacion.objects.create(factura=fact, operacion=opera)
                    opera.facturada = True
                    opera.save()
                messages.add_message(request, messages.SUCCESS, 'Factura agregada satisfactoriamente')
                return 1
            except:
                messages.add_message(request, messages.ERROR, 'Error al agregar factura. Contacte el Administrador !')
                return 0
        else:
            filePath = os.path.join(settings.BASE_DIR, "system/templates/prefactura_form.html")
            context = {'cliente': cliente, "operaciones": operaciones, "iva": iva, "subtotalmx": subtotalmx, \
                       "subtotalusd": subtotalusd, "totalmx": totalmx, "totalusd": totalusd}
            return render(request, filePath, context)
    else:
        raise Http404

@login_required
@ajax
@csrf_protect
def cancel_factura(request):
    if request.method == 'POST':
        factura = request.POST['factura']
        return True
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
                opera.append({"#": str(o.id), "fecha": o.fecha_inicio.strftime('%m/%d/%Y'), "cliente": str(o.cliente), \
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
@csrf_protect
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
@csrf_protect
def delconcepop(request):
    if request.method == 'POST':
        try:
            concep = Concepto_Operacion.objects.get(id=request.POST['concepto'])
            concep.delete()
            messages.add_message(request, messages.SUCCESS, 'Concepto eliminado satisfactoriamente')
            return True
        except:
            messages.add_message(request, messages.ERROR, 'Error al eliminar concepto. Contacte el Administrador !')
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
            filePath = os.path.join(settings.BASE_DIR, "system/templates/evento_form.html")
            context = {'form_evento': form}
            return render(request, filePath, context)
    raise Http404


@login_required
@ajax
@csrf_protect
def concepto_add(request):
    if request.method == 'POST':
        form = Concepto_Form(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Concepto agregado satisfactoriamente')
            return 1
        else:
            filePath = os.path.join(settings.BASE_DIR, "system/templates/concepto_form.html")
            context = {'form_concepto': form}
            return render(request, filePath, context)
    raise Http404


@method_decorator(login_required, name='dispatch')
class LogoutView(AJAXMixin, RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
