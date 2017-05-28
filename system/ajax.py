# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from django.conf import settings
import json
import os
from django.http import HttpResponse

@ajax
def prueba(request):
    r = request.POST['pais']
    filePath = os.path.join(settings.BASE_DIR, 'system\json\ciudades.json')
    ciudades = json.load(open(filePath))
    choice = []
    for c in ciudades:
        if c['value'] == request.POST['pais']:
            choice.append((c['value'], c['pais']))
    return choice
