# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from django.conf import settings
import json
import os
from django_ajax.mixin import AJAXMixin
from django.views.generic import RedirectView
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from system.models import *
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@login_required
@ajax
def get_ciudades(request):
    r = request.POST['pais']
    filePath = os.path.join(settings.BASE_DIR, 'system\json\ciudades.json')
    ciudades = json.load(open(filePath))
    choice = []
    for c in ciudades:
        if c['value'] == request.POST['pais']:
            choice.append((c['value'], c['pais']))
    return choice

@login_required
@ajax
def get_data_form(request):
    client = request.POST['cliente']
    choice = dict()
    extra = []
    cruce = []
    consig = []
    caja = []
    if client!='':
        servicios = Servicio.objects.filter(cliente=client)
        for c in servicios:
            try :
                service = Servicio_Cruce.objects.get(pk=c.id)
                cruce.append((service.id, service.get_tipo_display()))
            except:
                service = Servicio_Extra.objects.get(pk=c.id)
                extra.append((service.id, service.get_tipo_display()))
        consignatarios = Consignatario.objects.filter(cliente=client, usuario__is_active=True)
        for c in consignatarios:
            consig.append((c.id, c.usuario.first_name))
        cajas = Caja.objects.filter(cliente=client, fecha_entrada__lte=datetime.now(), fecha_salida__gt=datetime.now())
        for c in cajas:
            caja.append((c.id, c.numero))
        choice['cruce'] = cruce
        choice['extra'] = extra
        choice['consig'] = consig
        choice['caja'] = caja
    return choice

@login_required
@ajax
@csrf_protect
def startop(request):
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

@method_decorator(login_required, name='dispatch')
class LogoutView(AJAXMixin,RedirectView):
    url = '/login'
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

