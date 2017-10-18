# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from datetime import datetime


class CamionForm(forms.ModelForm):
    tipo_choices = (("0", "Libre"), ("2", "Arrendado"))
    estado = forms.ChoiceField(choices=tipo_choices, widget=forms.Select(attrs={'class': 'form-control', 'required': ''}))
    def __init__(self, *args, **kwargs):
        super(CamionForm, self).__init__(*args, **kwargs)
        if kwargs['instance']:
            if kwargs['instance'].estado == '1':
                del self.fields['estado']
    class Meta:
        model = Camion
        fields = ['numero', 'marca', 'modelo', 'serie', 'millaje', \
                  'placa', 'tag', 'decal', 'circulacion', 'expira_circulacion', 'estado']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', }),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control', }),
            'millaje': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', }),
            'tag': forms.TextInput(attrs={'class': 'form-control', }),
            'decal': forms.TextInput(attrs={'class': 'form-control', }),
            'circulacion': forms.TextInput(attrs={'class': 'form-control', }),
            'expira_circulacion': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),

        }


class OperadorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OperadorForm, self).__init__(*args, **kwargs)
        if kwargs['instance']:
            self.fields['camion'].queryset = Camion.objects.filter(estado=0, expira_circulacion__gt=datetime.now())\
                                             | Camion.objects.filter(id=kwargs['instance'].camion.id)
        else:
            self.fields['camion'].queryset = Camion.objects.filter(estado=0, expira_circulacion__gt=datetime.now())

    class Meta:
        model = Operador
        fields = ['nombre', 'direccion', 'ciudad', 'colonia', 'curp', 'pasaporte', 'telefono', 'celular', 'radio', \
                  'camion', 'nss', 'rfc', 'visa', 'visa_expira', \
                  'fast', 'fast_expira', 'licencia', 'licencia_expira', 'medico', 'medico_expira']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', }),
            'direccion': forms.TextInput(attrs={'class': 'form-control', }),
            'ciudad': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'colonia': forms.Select(attrs={'class': 'form-control select2'}),
            'pasaporte': forms.TextInput(attrs={'class': 'form-control', }),
            'telefono': forms.TextInput(attrs={'class': 'form-control', }),
            'celular': forms.TextInput(attrs={'class': 'form-control', }),
            'radio': forms.TextInput(attrs={'class': 'form-control', }),
            'camion': forms.Select(attrs={'class': 'form-control select2'}),
            'nss': forms.TextInput(attrs={'class': 'form-control', }),
            'curp': forms.TextInput(attrs={'class': 'form-control', }),
            'rfc': forms.TextInput(attrs={'class': 'form-control', }),
            'visa': forms.TextInput(attrs={'class': 'form-control', }),
            'visa_expira': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
            'fast': forms.TextInput(attrs={'class': 'form-control', }),
            'fast_expira': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
            'licencia': forms.TextInput(attrs={'class': 'form-control', }),
            'licencia_expira': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
            'medico': forms.TextInput(attrs={'class': 'form-control', }),
            'medico_expira': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
        }


class Vcamion_Form(forms.ModelForm):
    class Meta:
        model = Verificacion_Camion
        fields = ['camion_id', 'verificacion', 'expira']
        widgets = {
            'camion_id': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'verificacion': forms.TextInput(attrs={'class': 'form-control', }),
            'expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                                             "placeholder": "dd/mm/yyyy", }),
        }


class Icamion_Form(forms.ModelForm):
    class Meta:
        model = Inspeccion_Camion_US
        fields = ['camion_id', 'inspeccion', 'expira']
        widgets = {
            'camion_id': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'inspeccion': forms.TextInput(attrs={'class': 'form-control', }),
            'expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                                             "placeholder": "dd/mm/yyyy", }),
        }


class SMXcamion_Form(forms.ModelForm):
    class Meta:
        model = Seguromx_Camion
        fields = ['camion_id', 'seguromx', 'expira_seguromx']
        widgets = {
            'camion_id': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'seguromx': forms.TextInput(attrs={'class': 'form-control', }),
            'expira_seguromx': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
        }


class SUScamion_Form(forms.ModelForm):
    class Meta:
        model = Segurous_Camion
        fields = ['camion_id', 'segurous', 'expira_segurous']
        widgets = {
            'camion_id': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'segurous': forms.TextInput(attrs={'class': 'form-control', }),
            'expira_segurous': forms.DateInput(
                attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',
                       "placeholder": "dd/mm/yyyy", }),
        }


class Repcamion_Form(forms.ModelForm):
    class Meta:
        model = Reparacion_Camion
        fields = ['camion_id', 'rotura', 'fecha_inicio', 'fecha_fin', 'costo_mx', 'costo_usd', \
                  'detecto', 'detecto_fecha', 'supervisor', \
                  'supervisor_fecha', 'autorizo', 'autorizo_fecha', 'estado']
        widgets = {
            'camion_id': forms.Select(attrs={'class': 'form-control select2'}),
            'rotura': forms.TextInput(attrs={'class': 'form-control', }),
            'fecha_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'fecha_fin': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'costo_usd': forms.TextInput(attrs={'class': 'form-control'}),
            'costo_mx': forms.TextInput(attrs={'class': 'form-control'}),
            'detecto': forms.Select(attrs={'class': 'form-control select2'}),
            'supervisor': forms.Select(attrs={'class': 'form-control select2'}),
            'autorizo': forms.Select(attrs={'class': 'form-control select2'}),
            'detecto_fecha': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'supervisor_fecha': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'autorizo_fecha': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'estado': forms.CheckboxInput(
                attrs={'data-on-color': "success", 'data-off-color': "info", 'data-off-text': "Iniciada",
                       'data-on-text': "Terminada"}),
        }


class ORepcamion_Form(forms.ModelForm):
    class Meta:
        model = Orden_Reparacion_Camion
        fields = ['tipo', 'cantidad', 'provedor', 'factura', \
                  'costo_r_mx', 'costo_r_usd', 'tipo_pago', 'descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': ''}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'provedor': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'factura': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'costo_r_mx': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'costo_r_usd': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control', 'required': ''}),
        }

class Sellos_Form(forms.ModelForm):
    class Meta:
        model = Sello_Operacion
        fields = ['operacion', 'sello', 'fecha', 'observaciones']
        widgets = {
            'operacion': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'sello': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'fecha': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss", "onmouseover":"DataTime(this.id);"}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
        }

    def clean(self):
        cleaned_data = super(Sellos_Form, self).clean()
        fecha = cleaned_data.get('fecha')
        if fecha:
            fecha_ant = Sello_Operacion.objects.filter(fecha__gte=fecha).count()
            if fecha_ant > 0:
                self.add_error('fecha', 'La fecha debe ser mayor a la del sello anterior.')

class Evento_Form(forms.ModelForm):
    evento_choices = (("", "---------"), ("AMXV", "Aduana MX Verde"), ("AMXA", "Aduana MX Amarilla"),
                      ("AMXR", "Aduana MX Rojo"), \
                      ("AUSV", "Aduana US Verde"), ("AUSA", "Aduana US Amarrilla"), ("AUSR", "Aduana US Rojo"),
                      ("INSP", "Inspección"), \
                      ("RMP", "Rampa"), ("RX", "Rayos X"), ("DOT", "DOT"), ("FDA", "FDA"), ("PAMA", "PAMA"),
                      ("FIN", "Fin Operación"), ("CAN", "Cancelar Operación"))
    evento = forms.ChoiceField(choices=evento_choices, widget=forms.Select(attrs={ \
        'class': 'form-control', 'required': '', "onchange":"evento_select(this.value);"}))
    class Meta:
        model = Evento_Operacion
        fields = ['operacion', 'evento', 'fecha_inicio','fecha_terminacion', 'anden', 'vista', 'recibio', 'observaciones']
        widgets = {
            'operacion': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'evento': forms.Select(attrs={'class': 'form-control', 'required': '', "onchange":"evento_select(this.value);"}),
            'fecha_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss", "onmouseover":"DataTime(this.id);"}),
            'fecha_terminacion': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss", "onmouseover":"DataTime(this.id);"}),
            'anden': forms.TextInput(attrs={'class': 'form-control'}),
            'vista': forms.TextInput(attrs={'class': 'form-control'}),
            'recibio': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
        }

    def clean(self):
        cleaned_data = super(Evento_Form, self).clean()
        evento = cleaned_data.get('evento')
        operacion = cleaned_data.get('operacion')
        if evento == "CAN":
            if not cleaned_data.get('observaciones'):
                self.add_error('observaciones', 'Este campo es obligatorio')
            events = Evento_Operacion.objects.filter(evento="FIN", operacion=operacion).count()
            if events > 0:
                self.add_error('evento', 'No se puede cancelar operación finalizada ')
        if evento == "FIN":
            if not cleaned_data.get('recibio'):
                self.add_error('recibio', 'Este campo es obligatorio')
            if not cleaned_data.get('fecha_terminacion'):
                self.add_error('fecha_terminacion', 'Este campo es obligatorio')
        elif evento == "AMXR" or evento == "AUSR":
            if not cleaned_data.get('anden'):
                self.add_error('anden', 'Este campo es obligatorio')
            if not cleaned_data.get('vista'):
                self.add_error('vista', 'Este campo es obligatorio')
            if not cleaned_data.get('fecha_inicio'):
                self.add_error('fecha_inicio', 'Este campo es obligatorio')
        else:
            if not cleaned_data.get('fecha_inicio'):
                self.add_error('fecha_inicio', 'Este campo es obligatorio')

        events = Evento_Operacion.objects.filter(evento=evento, operacion=operacion).count()
        if events > 0:
            self.add_error('evento', 'Ya existe este evento en la operación')
        try:
            f_inicio = Evento_Operacion.objects.filter(fecha_inicio__gte=cleaned_data.get('fecha_inicio'), operacion=operacion).count()
            if f_inicio > 0:
                self.add_error('fecha_inicio', 'La fecha tiene que ser posterior a eventos anteriores')
        except:
            pass

class Concepto_Form(forms.ModelForm):
    class Meta:
        model = Concepto_Operacion
        fields = ['operacion', 'concepto', 'cantidad', 'costo_mx','costo_usd', 'observaciones']
        widgets = {
            'operacion': forms.TextInput(attrs={'style': 'visibility:hidden; position:absolute;'}),
            'concepto': forms.Select(attrs={'class': 'form-control', 'required': '', "onchange":"concepto_select(this.value);"}),
            'costo_usd': forms.TextInput(attrs={'class': 'form-control'}),
            'costo_mx': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
        }



class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', \
                  'is_superuser', ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
            'is_superuser': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
        }


class Cliente_Form(forms.ModelForm):
    usuario = forms.CharField(label=u"usuario", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'visibility:hidden; position:absolute;'}))

    class Meta:
        model = Cliente
        fields = ['usuario', 'pais', 'estado', 'direccion', 'cpostal', 'rfc', \
                  'telefono', 'tax', 'credito', 'facturacion', 'descripcion']
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-control select2'}),
            'estado': forms.Select(attrs={'class': 'form-control select2'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'cpostal': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', }),
            'tax': forms.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
            'facturacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'credito': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Contacto_Cliente_Form(forms.ModelForm):
    class Meta:
        model = Contactos_Cliente
        fields = ['contacto', 'tipo', 'email', 'telefono']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': ''})
        }


class Despachador_Cliente_Form(forms.ModelForm):
    class Meta:
        model = Despachador_Cliente
        fields = ['nombre', 'radio', 'telefono']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'radio': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
        }


class Consignatario_Form(forms.ModelForm):
    class Meta:
        model = Consignatario
        fields = ['cliente']


class Ejecutivo_Consignatario_Form(forms.ModelForm):
    class Meta:
        model = Ejecutivo_Consignatario
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': ''}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
        }


class Patio_Form(forms.ModelForm):
    class Meta:
        model = Patio
        fields = ['nombre', 'direccion', 'pais', 'linea', 'telefono', 'contacto', \
                  'latitud', 'longitud', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control select2'}),
            'linea': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.TextInput(attrs={'class': 'form-control'}),
            'longitud': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
        }


class Caja_Form(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['numero', 'cliente', 'fecha_entrada', 'fecha_salida', 'observaciones']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_entrada': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'fecha_salida': forms.DateTimeInput(
                attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',
                       "placeholder": "dd/mm/yyyy hh:ii:ss"}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 4}),
        }

    def clean(self):
        cleaned_data = super(Caja_Form, self).clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        if fecha_salida <= fecha_entrada:
            self.add_error('fecha_salida', 'Fecha de salida debe ser mayor a la de entrada.')


class Servicio_Cruce_Form(forms.ModelForm):

    class Meta:
        model = Servicio_Cruce
        fields = ['cliente', 'tipo', 'aduana', 'remolque', 'importemx', 'importeusd', 'iva']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
            'tipo': forms.Select(attrs={'class': 'form-control select2'}),
            'aduana': forms.Select(attrs={'class': 'form-control select2'}),
            'remolque': forms.Select(attrs={'class': 'form-control select2'}),
            'importemx': forms.TextInput(attrs={'class': 'form-control', 'disabled':''}),
            'importeusd': forms.TextInput(attrs={'class': 'form-control', 'disabled':''}),
            'iva': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
        }

    def clean(self):
        cleaned_data = super(Servicio_Cruce_Form, self).clean()
        importemx = cleaned_data.get('importemx')
        importeusd = cleaned_data.get('importeusd')
        if importemx == None and importeusd == None :
            self.add_error('importemx', 'Debe intoducir un importe al servicio')
            self.add_error('importeusd', 'Debe intoducir un importe al servicio')



class Servicio_Extra_Form(forms.ModelForm):
    class Meta:
        model = Servicio_Extra
        fields = ['cliente', 'tipo', 'importemx', 'importeusd', 'hlibres', 'iva']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
            'tipo': forms.Select(attrs={'class': 'form-control select2'}),
            'hlibres': forms.NumberInput(attrs={'class': 'form-control'}),
            'importemx': forms.TextInput(attrs={'class': 'form-control'}),
            'importeusd': forms.TextInput(attrs={'class': 'form-control'}),
            'iva': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
        }

class Operacion_Form(forms.ModelForm):
    sello = forms.CharField(label=u"Sello", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(Operacion_Form, self).__init__(*args, **kwargs)
        self.fields['operador'].queryset = Operador.objects.filter(estado=False, visa_expira__gt=datetime.now(), \
                                                                   fast_expira__gt=datetime.now(), licencia_expira__gt=datetime.now())
        self.fields['cliente'].queryset = Cliente.objects.filter(usuario__is_active=True)

    class Meta:
        model = Operacion
        fields = ['operador', 'cliente', 'consignatario', 'servicio', \
                  'origen', 'destino', 'caja', 'pedimento', 'referencia']
        widgets = {
            'operador': forms.Select(attrs={'class': 'form-control select2'}),
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
            'consignatario': forms.Select(attrs={'class': 'form-control select2'}),
            'servicio': forms.Select(attrs={'class': 'form-control select2'}),
            'pedimento': forms.TextInput(attrs={'class': 'form-control'}),
            'caja': forms.Select(attrs={'class': 'form-control select2'}),
            'origen': forms.Select(attrs={'class': 'form-control select2'}),
            'destino': forms.Select(attrs={'class': 'form-control select2'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(Operacion_Form, self).clean()
        origen = cleaned_data.get('origen')
        destino = cleaned_data.get('destino')
        sello = cleaned_data.get('sello')
        if origen == destino:
            self.add_error('origen', 'EL origen tiene que distinto al destino')
            self.add_error('destino', 'EL destino tiene que distinto al origen')
        sellos = Sello_Operacion.objects.filter(sello=sello).count()
        if sellos > 0:
            self.add_error('sello', 'Este sello ya fue utilizado.')


class Factura_Form(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2', 'required': ''}),
        }


class Resgistro_Form(UserCreationForm):
    username = forms.RegexField(label=u"Usuario", regex=r'^[a-z\d_]{4,15}$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Usuario")}))
    email = forms.EmailField(label=u"Correo", widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _(u"Correo")}))
    password1 = forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Contraseña")}))
    password2 = forms.CharField(label=u"Confirmar", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Confirmar contraseña")}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class Resgistro_User_Cliente_Form(UserCreationForm):
    email = forms.EmailField(label=u"Correo", widget=forms.EmailInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _(u"Correo")}))
    password1 = forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Contraseña")}))
    password2 = forms.CharField(label=u"Confirmar", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Confirmar contraseña")}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", 'first_name', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
        }


class Update_User_Cliente_Form(UserCreationForm):
    email = forms.EmailField(label=u"Correo", widget=forms.EmailInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _(u"Correo")}))

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'js-switch', 'data-color': "#66cc66", 'data-secondary-color': "#f96262", }),
        }


class EditPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Contraseña")}))
    new_password2 = forms.CharField(label=u"Confirmar", widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"Confirmar contraseña")}))
