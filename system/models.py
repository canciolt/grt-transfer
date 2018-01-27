# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin import models
from django.db import models
from  django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.validators import RegexValidator
from django.utils import timezone
from mixins import AuditMixin
from django.core.exceptions import ObjectDoesNotExist
import json
import os

telefono_regex = RegexValidator(regex=r'^\+?1?\d{10}$',message='Número de telefono invalido.')
cpostal_regex = RegexValidator(regex=r'^\+?1?\d{4,5}$', message='Código postal invalido.')
rfc_regex = RegexValidator(regex=r'^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$', message='Código RFC invalido')
lat_lon_regex = RegexValidator(regex=r'^-?([1-9]?[1-9]|[1-9]0)\.{1}\d{1,6}$', message='Coordenada invalida')
num_lett_regex = RegexValidator(regex=r'^[0-9a-zA-Z]+$', message='Numero de caja invalido')
curp_regex = RegexValidator(regex=r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$', message='CURP invalido')
nss_regex = RegexValidator(regex=r'^(\d{2})(\d{2})(\d{2})\d{5}$', message='Numero seguro social invalido')
pass_regex = RegexValidator(regex=r'^(\d{2})(\d{2})(\d{2})\d{5}$', message='Numero de pasaporte invalido')
licencia_regex = RegexValidator(regex=r'([A-ZÑ]{4})\d{6}', message='Numero de licencia invalido')
fast_regex = RegexValidator(regex=r'^\d{14}$', message='Numero de Fast invalido')
visa_regex = RegexValidator(regex=r'([A-ZÑ]{3})\d{9}', message='Numero de visa invalido')
medico_regex = RegexValidator(regex=r'^\d{6}$', message='Numero de medico invalido')

class Camion(AuditMixin, models.Model):
    tipo_choices = (("0", "Libre"), ("1", "Asignado"),("2", "Arrendado"))
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True, validators=[num_lett_regex], verbose_name="número")
    marca = models.CharField(max_length=50, verbose_name="marca")
    modelo = models.IntegerField(verbose_name="modelo")
    serie = models.CharField(unique=True, max_length=18, validators=[num_lett_regex], verbose_name="serie")
    millaje = models.IntegerField(default=0, verbose_name="millaje")
    placa = models.CharField(unique=True, max_length=8, validators=[num_lett_regex], verbose_name="placa")
    tag = models.IntegerField(verbose_name="TAG", help_text="Número de serie Tarjeta de cruze (Ida)")
    decal = models.IntegerField(verbose_name="DECAL", help_text="Número de serie Tarjeta de cruze (Regreso)")
    estado = models.CharField(max_length=2, choices=tipo_choices, default=0, verbose_name="estado", help_text="Seleccione si el camion esta arrendado")
    circulacion = models.CharField(max_length=20, validators=[num_lett_regex], verbose_name="circulación")
    expira_circulacion = models.DateField(verbose_name="vencimiento de circulación")
    fecha_estado = models.DateField(blank=True,null=True)

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
    pasaporte = models.CharField(max_length=15, validators=[pass_regex], verbose_name="pasaporte")
    telefono = models.CharField(blank=True, validators=[telefono_regex], max_length=10, verbose_name="teléfono")
    radio = models.CharField(blank=True, max_length=12, verbose_name="radio")
    celular = models.CharField(blank=True, max_length=10, validators=[telefono_regex], verbose_name="celular")
    camion = models.ForeignKey(Camion, null=True, on_delete=models.PROTECT)
    estado = models.BooleanField(default=False, verbose_name="estado", help_text="Seleccione estado (Libre-Ocupado)")
    nss = models.CharField(max_length=11, validators=[nss_regex], verbose_name="seguro social")
    curp = models.CharField(max_length=30, validators=[curp_regex], verbose_name="CURP")
    rfc = models.CharField(max_length=30, validators=[rfc_regex], verbose_name="registro de contribuyentes")
    visa = models.CharField(max_length=15, validators=[visa_regex], verbose_name="visa")
    visa_expira = models.DateField(verbose_name="vencimiento de visa")
    fast = models.CharField(max_length=15, validators=[fast_regex], verbose_name="cruse FAST")
    fast_expira = models.DateField(verbose_name="vencimiento de FAST")
    licencia = models.CharField(max_length=25, validators=[licencia_regex], verbose_name="licencia")
    licencia_expira = models.DateField(verbose_name="vencimiento de licencia")
    medico = models.CharField(max_length=25, validators=[medico_regex], verbose_name="seguro medico")
    medico_expira = models.DateField(verbose_name="vencimiento de seguro medico")

    def __str__(self):
        return self.nombre.encode('utf-8').strip()

class Combustible(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion, related_name="comb_camion", on_delete=models.CASCADE, verbose_name="camion")
    operador_id = models.ForeignKey(Operador, related_name="comb_operador", on_delete=models.CASCADE, verbose_name="operador")
    millaje = models.IntegerField(verbose_name="millaje")
    litros = models.FloatField(verbose_name="litros")
    fecha = models.DateTimeField()

    def __str__(self):
        return self.litros


class Pista(models.Model):
    id = models.AutoField(primary_key=True)
    litros = models.FloatField(verbose_name="litros")
    fecha = models.DateTimeField()

    def __str__(self):
        return self.fecha


class Reparacion_Camion(models.Model):
    id = models.AutoField(primary_key=True)
    camion_id = models.ForeignKey(Camion,null=False, blank=False, verbose_name="camion", on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(verbose_name="fecha de inicio")
    fecha_fin = models.DateTimeField(verbose_name="fecha de terminación")
    rotura = models.CharField(max_length=255, verbose_name="rotura")
    costo_usd = models.FloatField(verbose_name="costo USD")
    costo_mx = models.FloatField(verbose_name="costo MX")
    estado = models.BooleanField(default=False, verbose_name="estado reparación", help_text="Seleccione el estado (Iniciada-Terminada)")
    detecto = models.ForeignKey(Operador, verbose_name="detector de rotura", on_delete=models.PROTECT)
    detecto_fecha = models.DateTimeField(verbose_name="fecha de detección")
    supervisor = models.ForeignKey(User, related_name="supervisor_user", verbose_name="supervisor", on_delete=models.PROTECT)
    supervisor_fecha = models.DateTimeField(verbose_name="fecha de supervición")
    autorizo = models.ForeignKey(User, related_name="autorizo_user", verbose_name="autorizo", on_delete=models.PROTECT)
    autorizo_fecha = models.DateTimeField(verbose_name="fecha de autorización")

    def __str__(self):
        return self.id


class Orden_Reparacion_Camion(models.Model):
    tipo_choices = (("P", "Cambio de Pieza"), ("MO", "Mano de obra"))
    pago_choices = (("E", "Efectivo"), ("CH", "Cheque"))
    id = models.AutoField(primary_key=True)
    reparacion_id = models.ForeignKey(Reparacion_Camion, verbose_name="reparación ID", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, verbose_name="descripcion")
    tipo = models.CharField(max_length=2, choices=tipo_choices, verbose_name="tipo de reparacion")
    cantidad = models.IntegerField(verbose_name="cantida")
    provedor = models.CharField(max_length=150, verbose_name="provedor")
    factura = models.CharField(max_length=17, verbose_name="factura")
    costo_r_mx = models.FloatField(verbose_name="costo MX")
    costo_r_usd = models.FloatField(verbose_name="costo US")
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
    descripcion = models.TextField(verbose_name="motivo de la multa")
    expira = models.DateField(verbose_name="vigencia de la Multa")
    grua = models.CharField(max_length=25, blank=True, verbose_name="grua")
    importe_grua = models.FloatField(default=0, verbose_name="importe de grua")
    estado = models.BooleanField(default=0, choices=estado_multa, verbose_name="estado de la multa")

    def __str__(self):
        return self.numero

def get_pais():
    filePath = os.path.join(settings.BASE_DIR, 'system\json\paises.json')
    paises = json.load(open(filePath))
    choice = []
    for pais in paises:
        choice.append((pais['value'], pais['pais']))
    return choice

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    pais = models.CharField(choices=get_pais(),max_length=20, verbose_name="país")
    estado = models.CharField(max_length=20, verbose_name="estado")
    direccion = models.CharField(max_length=70, verbose_name="dirección")
    cpostal = models.CharField(max_length=5, validators=[cpostal_regex], verbose_name="código postal")
    rfc = models.CharField(max_length=13, validators=[rfc_regex], verbose_name="RFC", blank=True, help_text='Registro Federal de Contribuyentes')
    telefono = models.CharField(max_length=10,validators=[telefono_regex], verbose_name="teléfono")
    descripcion = models.TextField(verbose_name="descripcion", blank=True)
    tax = models.CharField(max_length=45, verbose_name="tax", blank=True)
    credito = models.IntegerField(verbose_name="credito")
    facturacion = models.IntegerField(verbose_name="facturación", help_text="Días de facturación")


    def __str__(self):
        return self.usuario.first_name

    def delete(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.usuario.id)
        super(Cliente, self).delete(*args, **kwargs)
        user.delete()

class Contactos_Cliente(models.Model):
    tipo_choices = (("IMP", "Importación"), ("EXP", "Exportación"), \
                    ("FACMX", "Facturación MX"), ("FACUS", "Facturación US"))
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=50, verbose_name="contacto")
    tipo = models.CharField(choices=tipo_choices, max_length=20, verbose_name="tipo")
    telefono = models.CharField(max_length=10, validators=[telefono_regex], verbose_name="telefono")
    email = models.EmailField(unique=True,verbose_name="correo")

    def __str__(self):
        return self.numero

class Consignatario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.first_name

    def delete(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.usuario.id)
        super(Consignatario, self).delete(*args, **kwargs)
        user.delete()

class Ejecutivo_Consignatario(models.Model):
    id = models.AutoField(primary_key=True)
    consignatario = models.ForeignKey(Consignatario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70, verbose_name="ejecutivo")
    telefono = models.CharField(max_length=10, validators=[telefono_regex], verbose_name="telefono")
    email = models.EmailField(verbose_name="correo")

    def __str__(self):
        return self.nombre

class Despachador_Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, verbose_name="nombre")
    radio = models.CharField(max_length=20, blank=True, verbose_name="radio")
    telefono = models.CharField(max_length=10, validators=[telefono_regex], verbose_name="telefono")

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    importemx = models.FloatField(verbose_name="importe MX")
    importeusd = models.FloatField(verbose_name="importe USD")
    iva = models.BooleanField(default=False, verbose_name="aplica IVA")
    retencion = models.BooleanField(default=False, verbose_name="aplica Retencion del 4%")

    def __str__(self):
        try:
            return str(self.servicio_cruce)
        except ObjectDoesNotExist:
            return str(self.servicio_extra)


class Servicio_Cruce(Servicio):
    tipo_choices = (("T", "Trompo"), ("TUS", "Trompo US"), ("TMX", "Trompo MX"), ("R", "Repartos"),
                    ("ML", "Movimiento local"), ("MLMX", "Movimiento local MX"), ("MLUS", "Movimiento local US"), \
                    ("MLR", "Movimiento local Rampa"), ("EXP", "Exportación"), ("EXPV", "Exportación vacia"), ("IMP", "Importación"), \
                    ("IMPV", "Importación vacia"), ("MP", "Movimiento de patio"), ("MPUS", "Movimiento de patio US"),("MPMX", "Movimiento de patio MX"), \
                    ("MP", "Movimiento de inspección"),("CF", "Cruze en falso"), ("CFMX", "Cruze en falso MX"), ("CFUS", "Cruze en falso US"))
    aduana_choices = (("LRD-240", "Laredo-240"), ("COL-800", "Colombia-800"))
    remolque_choices = (("NO", "No aplica"), ("CS", "Caja seca"), ("CSE", "Caja seca Esp."), ("CSV", "aja seca vacia"), \
                        ("CSH", "Caja seca Hazmat"), ("C", "Contenedor"), ("P", "Plataforma"), ("PE", "Plataforma Esp."), \
                        ("SL", "Semi Lowboy"), ("L", "Lowboy"), ("PP", "Poppies"), ("R", "Refrigerada"), ("PA", "Pipa"))
    tipo = models.CharField(choices=tipo_choices, max_length=25, verbose_name="tipo de servicio")
    aduana = models.CharField(choices=aduana_choices, max_length=50, verbose_name="aduana")
    remolque = models.CharField(choices=remolque_choices, max_length=50, verbose_name="remolque")

    def __str__(self):
        return (self.get_tipo_display()+" | "+self.get_aduana_display()+" | "+self.get_remolque_display()).encode('utf-8').strip()

class Servicio_Extra(Servicio):
    tipo_choices = (("AGR", "Agricultura"), ("AMA", "Amarres"), ("BAS", "Bascula"), ("CE", "Costo Extraordinario"),
                    ("CF", "Cruce en Falso"), ("CFP3", "Cruce en Falso Puente 3"), ("CFC", "Cruce en Falso Colombia"), \
                    ("DEM", "Demoras"), ("DES", "Descuento"), ("DFI", "Dia Festivo Impo."), ("DFE", "Dia Festivo Expo."), \
                    ("EE", "Eje Extra"), ("HM", "Haz-Mat"), ("I", "Inspección"),("ICB", "Inspección Costo Base"), \
                    ("ICBT", "Inspección Costo Base T"),("MF", "Movimiento en Falso"), ("S5000", "Sobrepeso de 1 a 5000 Lb"), \
                    ("S+5000", "Sobrepeso de +5000 Lb"), ("MC", "Multa Caja"), ("SC", "Servicio de Corte"),("Ref", "Refacturación"), \
                    ("Rep", "Repartos"),("RC", "Renta de Caja"),("RV", "Retorno Vacio"),("RAMX", "Rojo Aduana MX"),("RAUS", "Rojo Aduana US"), \
                    ("Pen", "Pension"),("Per", "Permisos"),("GxC", "Grua x Colombia"), ("GxL", "Grua x Laredo"),("Repa", "Reparación"), \
                    ("Wal", "Walmart"))
    tipo = models.CharField(choices=tipo_choices, max_length=25, verbose_name="tipo de servicio")
    hlibres = models.IntegerField(verbose_name="horas libres")

    def __str__(self):
        return self.get_tipo_display().encode('utf-8').strip()


class Patio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="nombre")
    direccion = models.CharField(max_length=70, verbose_name="dirección")
    pais = models.CharField(choices=get_pais(), max_length=20, verbose_name="país")
    linea = models.CharField(max_length=50, verbose_name="linea")
    telefono = models.CharField(max_length=20,validators=[telefono_regex], verbose_name="telefono")
    contacto = models.CharField(max_length=50, verbose_name="contacto")
    observaciones = models.TextField(verbose_name="observaciones", blank=True)
    latitud = models.CharField(max_length=50, validators=[lat_lon_regex], verbose_name="latitud")
    longitud = models.CharField(max_length=50, validators=[lat_lon_regex], verbose_name="longitud")

    def __str__(self):
        return self.nombre

class Operacion(models.Model):
    estado_choices = (("P", "Pendiente autorización"),("I", "Iniciada"),("T", "Terminada"),("C", "Cancelada"))
    id = models.AutoField(primary_key=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="servicio")
    fecha_inicio = models.DateTimeField(verbose_name="fecha de inicio")
    operador = models.ForeignKey(Operador, on_delete=models.PROTECT, verbose_name="operador")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name="cliente")
    caja = models.CharField(max_length=30,  verbose_name="caja")
    consignatario = models.ForeignKey(Consignatario, verbose_name="consignatario")
    origen = models.ForeignKey(Patio, related_name="patio_origen", verbose_name="origen")
    destino = models.ForeignKey(Patio, related_name="patio_destino", verbose_name="destino")
    estado = models.CharField(max_length=20, choices=estado_choices, default="P",  verbose_name="estado operación")
    referencia = models.CharField(max_length=15, verbose_name="referencia")
    pedimento = models.CharField(max_length=15, verbose_name="pedimento")
    facturada = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Evento_Operacion(models.Model):
    evento_choices = (("INIT", "Inicio de Opereción"),("AMXV", "Aduana MX Verde"),("AMXA", "Aduana MX Amarilla"), ("AMXR", "Aduana MX Rojo"), \
        ("AUSV", "Aduana US Verde"),("AUSA", "Aduana US Amarrilla"),("AUSR", "Aduana US Rojo"),("INSP", "Inspección"), \
        ("RMP", "Rampa"), ("RX", "Rayos X"), ("DOT", "DOT"), ("FDA", "FDA"), ("PAMA", "PAMA"), ("FIN", "Fin Operación"), ("CAN", "Cancelar Operación"))
    id = models.AutoField(primary_key=True)
    evento = models.CharField(choices=evento_choices, max_length=5, verbose_name="evento")
    operacion = models.ForeignKey(Operacion,on_delete=models.PROTECT, verbose_name="operacion")
    fecha_inicio = models.DateTimeField(blank=True, null=True, verbose_name="fecha de inicio")
    fecha_terminacion = models.DateTimeField(blank=True, null=True, verbose_name="fecha de terminación")
    anden = models.CharField(max_length=5, blank=True, null=True, verbose_name="anden")
    vista = models.CharField(max_length=35, blank=True, null=True, verbose_name="vista")
    recibio = models.CharField(max_length=30, blank=True, null=True, verbose_name="recibio")
    observaciones = models.TextField(blank=True, null=True, verbose_name="observaciones")

    def __str__(self):
        return self.evento

class Concepto_Operacion(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField(max_length=50, verbose_name="concepto")
    fecha_concepto = models.DateTimeField(verbose_name="fecha de concepto")
    operacion = models.ForeignKey(Operacion,on_delete=models.PROTECT, verbose_name="operacion")
    costo_usd = models.FloatField(verbose_name="costo USD")
    costo_mx = models.FloatField(verbose_name="costo MX")
    observaciones = models.TextField(verbose_name="observaciones")

    def __str__(self):
        return self.concepto

class Sello_Operacion(models.Model):
    id = models.AutoField(primary_key=True)
    operacion = models.ForeignKey(Operacion, on_delete=models.PROTECT,  verbose_name="operacion" )
    sello = models.CharField(max_length=50, unique=True, verbose_name="sello")
    fecha = models.DateTimeField(verbose_name="Fecha")
    observaciones = models.TextField(blank=True, verbose_name="observaciones")

    def __str__(self):
        return self.sello

class Factura(models.Model):
    estado_choices = (("A", "Abierta"), ("C", "Cancelada"), ("P", "Pagada"))
    id = models.AutoField(primary_key=True)
    nfactura = models.CharField(max_length=11, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    expira = models.DateTimeField()
    pagada = models.BooleanField(default=False)
    total_usd = models.FloatField(blank=True, null=True, verbose_name="total USD")
    total_mx = models.FloatField(blank=True, null=True, verbose_name="total MX")
    estado = models.CharField(choices=estado_choices, default='A', max_length=1)
    tasa_cambio = models.FloatField(default=0)
    observaciones = models.TextField(blank=True, verbose_name="observaciones")

    def __str__(self):
        return self.nfactura

class Factura_Operacion(models.Model):
    id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, verbose_name="factura")
    operacion = models.ForeignKey(Operacion, on_delete=models.PROTECT, verbose_name="operacion")

    def __str__(self):
        return self.operacion

class Tasa_Cambio(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(unique=True)
    tasa = models.FloatField(verbose_name="tasa de cambio")

    def __str__(self):
        return self.tasa

class Pagos(models.Model):
    moneda_choices = (("MXN", "Pesos"), ("USD", "Dollar"))
    metodo_choices = (("C", "Cheque"), ("T", "Transferencia"))
    estado_choices = (("P", "Pendiente"), ("A", "Aprobado"), ("C", "Cancelado"))
    cuenta_choices = (("IBC", "IBC"), ("BMEX", "Banamex"), ("GRT", "Grt-transfer"))
    id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, verbose_name="factura")
    moneda = models.CharField(choices=moneda_choices, max_length=3)
    importe = models.FloatField(verbose_name="importe a pagar")
    fecha = models.DateTimeField(verbose_name="fecha de pago")
    metodo = models.CharField(choices=metodo_choices, max_length=1, verbose_name="metodo de pago")
    estado = models.CharField(choices=estado_choices, default='P', max_length=1)
    cuenta = models.CharField(choices=cuenta_choices, max_length=4, verbose_name="Cuenta de deposito")
    observaciones = models.TextField(blank=True, verbose_name="observaciones")

    def __str__(self):
        return self.id