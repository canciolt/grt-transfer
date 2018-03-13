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
from system.forms import *
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
            choice['cruce'] = cruce
            choice['extra'] = extra
            choice['consig'] = consig
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
        retencion = 0
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
            if temp_op.servicio.retencion == True:
                retencion += imp_mxn * 0.04
            for conc in conc_operacion:
                subtotalusd += conc.costo_usd
                subtotalmx += conc.costo_mx
                if temp_op.servicio.iva == True:
                    iva += conc.costo_mx * 0.16
                if temp_op.servicio.retencion == True:
                    retencion += conc.costo_mx * 0.04
            operaciones.append({"id": temp_op.id, "fecha": temp_op.fecha_inicio, "servicio": temp_op.servicio, \
                                "consignatario": temp_op.consignatario, "importeusd": imp_usd, "importemxn": imp_mxn,
                                "conceptos": conc_operacion})
        totalmx += subtotalmx + iva - retencion
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
                                                  total_mx=round(mx, 2), tasa_cambio=tasa)
                else:
                    fact = Factura.objects.create(nfactura=nfactura, cliente=cliente, expira=expira,
                                                  total_usd=round(totalusd, 2), \
                                                  total_mx=round(totalmx, 2), tasa_cambio=tasa)
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
            context = {'cliente': cliente, "operaciones": operaciones, "iva": iva, "retencion": retencion, "subtotalmx": subtotalmx, \
                       "subtotalusd": subtotalusd, "totalmx": totalmx, "totalusd": totalusd}
            return render(request, filePath, context)
    else:
        raise Http404


@login_required
@ajax
@csrf_protect
def cancel_factura(request):
    if request.method == 'POST':
        if 'factura' in request.POST:
            nfactura = request.POST['factura']
            factura = get_object_or_404(Factura, nfactura=nfactura)
            payments = Pagos.objects.filter(factura=factura).count()
            if payments == 0:
                operaciones = Factura_Operacion.objects.filter(factura=factura)
                for op in operaciones:
                    op.operacion.facturada = False
                    op.operacion.save()
                factura.estado = "C"
                factura.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Factura cancelada satisfactoriamente !')
                return True
            else:
                messages.add_message(request, messages.ERROR,
                                     'Esta Factura tiene pagos asociados por lo que no se puede cancelar !')
                return False
        else:
            return False
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
def add_payment(request):
    if request.method == 'POST':
        form = Pagos_Form(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Pago agregado satisfactoriamente')
            return 1
        else:
            filePath = os.path.join(settings.BASE_DIR, "system/templates/payment_form.html")
            context = {'form_payment': form}
            return render(request, filePath, context)
    raise Http404

@login_required
@ajax
@csrf_protect
def add_comb(request):
    if request.method == 'POST':
        if 'camion' in request.POST:
            camion_id = request.POST['camion']
            form = Combustible_Form(initial={"camion_id": camion_id})
            filePath = os.path.join(settings.BASE_DIR, "system/templates/combustible_form.html")
            context = {'form_comb': form}
            return render(request, filePath, context)
        else:
            form = Combustible_Form(data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Combustible agregado satisfactoriamente')
                return 1
            else:
                filePath = os.path.join(settings.BASE_DIR, "system/templates/combustible_form.html")
                context = {'form_comb': form}
                return render(request, filePath, context)
    raise Http404

@login_required
@ajax
@csrf_protect
def add_comb_pista(request):
    if request.method == 'POST':
        form = Pista_Form(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Pista habilitada satisfactoriamente')
            return 1
        else:
            filePath = os.path.join(settings.BASE_DIR, "system/templates/pista_form.html")
            context = {'pista_form': form}
            return render(request, filePath, context)
    raise Http404


@login_required
@ajax
@csrf_protect
def startpay(request):
    if request.method == 'POST':
        if 'payid' in request.POST:
            payid = request.POST['payid']
            payment = get_object_or_404(Pagos, pk=int(payid))
            payment.estado = 'A'
            payment.save()
            payments = Pagos.objects.filter(factura=payment.factura, estado='A')
            pagosmxn = 0
            pagosusd = 0
            for p in payments:
                if p.moneda == "MXN":
                    pagosmxn += p.importe
                if p.moneda == "USD":
                    pagosusd += p.importe
            if payment.factura.total_usd == 0 and payment.factura.total_mx > 0:
                if payment.factura.total_mx == pagosmxn:
                    payment.factura.estado = "P"
                    payment.factura.save()

            if payment.factura.total_usd > 0 and payment.factura.total_mx == 0:
                if payment.factura.total_usd == pagosusd:
                    payment.factura.estado = "P"
                    payment.factura.save()
            if payment.factura.total_usd > 0 and payment.factura.total_mx > 0:
                if payment.factura.total_usd == pagosusd and payment.factura.total_mx == pagosmxn:
                    payment.factura.estado = "P"
                    payment.factura.save()

        else:
            return 0
    else:
        raise Http404


@login_required
@ajax
@csrf_protect
def checkmoney(request):
    if request.method == 'POST':
        if 'factura' in request.POST:
            nfactura = request.POST['factura']
            factura = get_object_or_404(Factura, pk=nfactura)
            pagos = Pagos.objects.filter(factura=factura)
            totalpagosmxn = 0
            totalpagosusd = 0
            for p in pagos:
                if p.moneda == "MXN":
                    totalpagosmxn += p.importe
                if p.moneda == "USD":
                    totalpagosusd += p.importe
            if factura.total_mx == 0 and factura.total_usd > 0:
                return {"moneda": "USD", "importe": round(factura.total_usd - totalpagosusd, 2)}
            if factura.total_mx > 0 and factura.total_usd == 0:
                return {"moneda": "MXN", "importe": round(factura.total_mx - totalpagosmxn, 2)}
            if factura.total_mx > 0 and factura.total_usd > 0:
                return {"moneda": "MXN-USD", "importemxn": round(factura.total_mx - totalpagosmxn, 2),
                        "importeusd": round(factura.total_usd - totalpagosusd, 2)}
        else:
            return False
    raise Http404

@login_required
@ajax
@csrf_protect
def report_main(request):
    if request.method == 'POST':
        payments = Pagos.objects.filter(estado="A")
        cxc = Factura.objects.filter(estado='A').count()
        ingmxn = 0
        ingusd = 0
        for p in payments:
            if p.moneda == 'MXN':
                ingmxn += p.importe
            if p.moneda == 'USD':
                ingusd += p.importe
        return {"ingmxn":ingmxn, "ingusd":ingusd, "pagos":payments.count(), "cxc":cxc}
    raise Http404


@login_required
@ajax
@csrf_protect
def get_payments_client(request):
    if request.method == 'POST':
        if 'cliente' in request.POST:
            cliente = request.POST['cliente']
            payments = []
            mxn = 0
            usd = 0
            pagos = Pagos.objects.filter(factura__cliente= cliente, estado='A').order_by('-fecha', 'factura')
            fp = Factura.objects.filter(cliente= cliente, estado= 'A').count()
            fv = Factura.objects.filter(cliente= cliente, estado= 'A', expira__lt= timezone.now()).count()
            for p in pagos:
                fvencimiento = p.factura.expira
                fpago = p.fecha
                if fpago > fvencimiento:
                    dvencidos = fpago - fvencimiento
                else:
                    dvencidos = 0
                payments.append(
                    {"factura": p.factura, "fecha": p.fecha, "metodo": p.get_metodo_display, \
                     "cuenta": p.get_cuenta_display, "importe": p.importe, "moneda": p.moneda, "dvencidos": dvencidos})
                if p.moneda == 'MXN':
                    mxn += p.importe
                if p.moneda == 'USD':
                    usd += p.importe
            filePath = os.path.join(settings.BASE_DIR, "system/templates/payments_client.html")
            context = {'payments': payments, 'mxn':mxn, 'usd':usd, 'fp':fp, 'fv':fv}
            return render(request, filePath, context)
        else:
            raise Http404
    else:
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
            if request.POST['evento'] == "FIN":
                operacion = get_object_or_404(Operacion, pk=request.POST['operacion'])
                operacion.estado = "T"
                operacion.save()
                ope = get_object_or_404(Operador, pk=operacion.operador.id)
                ope.estado = False
                ope.save()
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
