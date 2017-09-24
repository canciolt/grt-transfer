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
def get_servicios(request):
    client = request.POST['cliente']
    servicios = Servicio.objects.filter(cliente=client)
    choice = []
    for c in servicios:
        choice.append((c.id, c.))
    return choice

@method_decorator(login_required, name='dispatch')
class LogoutView(AJAXMixin,RedirectView):
    url = '/login'
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
