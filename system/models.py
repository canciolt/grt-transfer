# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from  django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator
import json
import os


class Camion(models.Model):
    tipo_choices = (("0", "Libre"), ("1", "Ocupado"),("2", "Arrendado"))
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True, verbose_name="número")
    marca = models.CharField(max_length=50, verbose_name="marca")
    modelo = models.IntegerField(verbose_name="modelo")
    serie = models.CharField(unique=True, max_length=18, verbose_name="serie")
    millaje = models.IntegerField(default=0, verbose_name="millaje")
    placa = models.CharField(unique=True, max_length=8, verbose_name="placa")
    tag = models.IntegerField(verbose_name="TAG", help_text="Número de serie Tarjeta de cruze (Ida)")
    decal = models.IntegerField(verbose_name="DECAL", help_text="Número de serie Tarjeta de cruze (Regreso)")
    estado = models.CharField(max_length=2,choices=tipo_choices, default=0, verbose_name="estado")
    circulacion = models.CharField(max_length=20, verbose_name="circulación")
    expira_circulacion = models.DateField(verbose_name="vencimiento de circulación")


    class Meta:
        verbose_name = "Camion"
        verbose_name_plural = "Camiones"

    def __str__(self):
        return str(self.numero)


class Ubicacion_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, related_name="uc_camion", on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=100)
    fecha = models.DateTimeField()

    def __str__(self):
        return self.ubicacion

class Seguromx_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, related_name="smx_camion", on_delete=models.CASCADE)
    seguromx = models.CharField(max_length=20, verbose_name="seguro MX")
    expira_seguromx = models.DateField(verbose_name="vencimiento de seguro MX")

    def __str__(self):
        return self.seguromx

class Segurous_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, related_name="sus_camion", on_delete=models.CASCADE)
    segurous = models.CharField(max_length=20, verbose_name="seguro US")
    expira_segurous = models.DateField(verbose_name="vencimiento de seguro US")

    def __str__(self):
        return self.segurous

class Inspeccion_Camion_US(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, on_delete=models.CASCADE)
    inspeccion = models.CharField(max_length=20, verbose_name="inspección")
    expira = models.DateField(unique=True, verbose_name="vencimiento de inspección")

    def __str__(self):
        return self.camion_id


class Verificacion_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, on_delete=models.CASCADE)
    verificacion = models.CharField(max_length=20, verbose_name="verificación")
    expira = models.DateField(unique=True, verbose_name="vencimiento de verificación")

    def __str__(self):
        return self.camion_id

    class Meta:
        verbose_name = "verificación camion"
        verbose_name_plural = "verificación camion"


def get_colonia():
    filePath = os.path.join(settings.BASE_DIR, 'system\json\colonias.json')
    colonias = json.loads(open(filePath).read())
    choice = []
    for c in colonias:
        choice.append((c, c))
    return choice


class Operador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="nombre")
    direccion = models.CharField(max_length=50, verbose_name="dirección")
    colonia = models.CharField(choices=get_colonia(), max_length=20, verbose_name="colonia")
    ciudad = models.CharField(max_length=20, default="Nuevo Laredo", verbose_name="ciudad")
    pasaporte = models.CharField(max_length=15, verbose_name="pasaporte")
    telefono = models.CharField(blank=True, max_length=10, verbose_name="teléfono")
    radio = models.CharField(blank=True, max_length=12, verbose_name="radio")
    celular = models.CharField(blank=True, max_length=10, verbose_name="celular")
    camion = models.ForeignKey(Camion, null=True, on_delete=models.SET_NULL)
    estado = models.BooleanField(default=False, verbose_name="estado", help_text="Seleccione estado (Libre-Ocupado)")
    nss = models.CharField(max_length=30, verbose_name="seguro social")
    curp = models.CharField(max_length=30, verbose_name="CURP")
    rfc = models.CharField(max_length=30, verbose_name="registro de contribuyentes")
    visa = models.CharField(max_length=15, verbose_name="visa")
    visa_expira = models.DateField(verbose_name="vencimiento de visa")
    fast = models.CharField(max_length=15, verbose_name="cruse FAST")
    fast_expira = models.DateField(verbose_name="vencimiento de FAST")
    licencia = models.CharField(max_length=25, verbose_name="licencia")
    licencia_expira = models.DateField(verbose_name="vencimiento de licencia")
    medico = models.CharField(max_length=25, verbose_name="seguro medico")
    medico_expira = models.DateField(verbose_name="vencimiento de seguro medico")

    def __str__(self):
        return self.nombre.encode('utf-8').strip()


class Reparacion_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion,null=False, blank=False, verbose_name="camion", on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(verbose_name="fecha de inicio")
    fecha_fin = models.DateTimeField(verbose_name="fecha de terminación")
    rotura = models.CharField(max_length=255, verbose_name="rotura")
    costo_usd = models.FloatField(verbose_name="costo USD")
    costo_mx = models.FloatField(verbose_name="costo MX")
    estado = models.BooleanField(default=False, verbose_name="estado reparación", help_text="Seleccione el estado (Iniciada-Terminada)")
    detecto = models.ForeignKey(Operador, verbose_name="Detector de rotura", on_delete=models.PROTECT)
    detecto_fecha = models.DateTimeField(verbose_name="fecha de detección")
    supervisor = models.ForeignKey(User, related_name="supervisor_user", verbose_name="Supervisor", on_delete=models.PROTECT)
    supervisor_fecha = models.DateTimeField(verbose_name="fecha de supervición")
    autorizo = models.ForeignKey(User, related_name="autorizo_user", verbose_name="Autorizo", on_delete=models.PROTECT)
    autorizo_fecha = models.DateTimeField(verbose_name="fecha de autorización")

    def __str__(self):
        return self.id


class Orden_Reparacion_Camion(models.Model):
    tipo_choices = (("P", "Cambio de Pieza"), ("MO", "Mano de obra"))
    pago_choices = (("E", "Efectivo"), ("CH", "Cheque"))
    id = models.AutoField(primary_key=True)
    reparacion_id = models.ForeignKey(Reparacion_Camion, verbose_name="reparación ID", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, verbose_name="descripcion")
    tipo = models.CharField(max_length=2, choices=tipo_choices, verbose_name="tipo de Reparacion")
    cantidad = models.IntegerField(verbose_name="cantida")
    provedor = models.CharField(max_length=150, verbose_name="provedor")
    factura = models.CharField(max_length=17, verbose_name="factura")
    costo_r_mx = models.FloatField(verbose_name="Costo MX")
    costo_r_usd = models.FloatField(verbose_name="Costo US")
    tipo_pago = models.CharField(max_length=2, choices=pago_choices, verbose_name="tipo de pago")

    def __str__(self):
        return self.factura


class Multas_Camion(models.Model):
    estado_multa = ((0, "Pendiente de pago"), (1, "Pagado"))
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, verbose_name="camion", on_delete=models.CASCADE)
    fecha_multa = models.DateTimeField(verbose_name="fecha de multa")
    numero = models.IntegerField(unique=True, verbose_name="número de multa")
    importe = models.FloatField(verbose_name="importe de multa")
    descripcion = models.TextField(verbose_name="Motivo de la multa")
    expira = models.DateField(verbose_name="Vigencia de la Multa")
    grua = models.CharField(max_length=25, blank=True, verbose_name="grua")
    importe_grua = models.FloatField(default=0, verbose_name="importe de grua")
    estado = models.BooleanField(default=0, choices=estado_multa, verbose_name="estado de la multa")

    def __str__(self):
        return self.numero


class Flujo_Trabajo(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(User)
    ip = models.GenericIPAddressField()
    modulo = models.CharField(max_length=250)
    navegador = models.CharField(max_length=250)
