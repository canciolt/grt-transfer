# -*- coding: utf-8 -*-
from django import forms
from models import Camion, Operador, Verificacion_Camion, Inspeccion_Camion_US, \
                   Reparacion_Camion, Orden_Reparacion_Camion, Seguromx_Camion,\
                   Segurous_Camion




class CamionForm(forms.ModelForm):

   class Meta:
      model = Camion
      fields = ['numero','marca','modelo','serie','millaje',\
                'placa','tag','decal','circulacion','expira_circulacion','estado']
      widgets = {
         'numero': forms.TextInput(attrs={'class': 'form-control'}),
          'marca': forms.TextInput(attrs={'class': 'form-control',}),
          'modelo': forms.TextInput(attrs={'class': 'form-control'}),
          'serie': forms.TextInput(attrs={'class': 'form-control', }),
          'millaje': forms.TextInput(attrs={'class': 'form-control'}),
          'placa': forms.TextInput(attrs={'class': 'form-control', }),
          'tag': forms.TextInput(attrs={'class': 'form-control', }),
          'decal': forms.TextInput(attrs={'class': 'form-control', }),
          'estado': forms.Select(attrs={'class': 'form-control'}),
          'circulacion': forms.TextInput(attrs={'class': 'form-control', }),
          'expira_circulacion': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format":'dd/mm/yyyy', "placeholder":"dd/mm/yyyy", }),


      }

class OperadorForm(forms.ModelForm):

   class Meta:
      model = Operador
      fields = ['nombre', 'direccion', 'ciudad', 'colonia','curp', 'pasaporte', 'telefono','celular','radio',\
                'camion', 'nss','rfc', 'visa', 'visa_expira', \
                'fast', 'fast_expira', 'licencia', 'licencia_expira', 'medico', 'medico_expira', 'estado']
      widgets = {
          'nombre': forms.TextInput(attrs={'class': 'form-control',}),
          'direccion': forms.TextInput(attrs={'class': 'form-control', }),
          'ciudad': forms.TextInput(attrs={'style':'visibility:hidden; position:absolute;'}),
          'colonia': forms.Select(attrs={'class': 'form-control select2'}),
          'pasaporte': forms.TextInput(attrs={'class': 'form-control', }),
          'telefono': forms.TextInput(attrs={'class': 'form-control', }),
          'celular': forms.TextInput(attrs={'class': 'form-control', }),
          'radio': forms.TextInput(attrs={'class': 'form-control', }),
          'camion': forms.Select(attrs={'class': 'form-control select2'}),
          'estado': forms.CheckboxInput(attrs={'class': 'js-switch', 'data-color': "#f96262", 'data-secondary-color': "#66cc66", }),
          'nss': forms.TextInput(attrs={'class': 'form-control', }),
          'curp': forms.TextInput(attrs={'class': 'form-control', }),
          'rfc': forms.TextInput(attrs={'class': 'form-control', }),
          'visa': forms.TextInput(attrs={'class': 'form-control', }),
          'visa_expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',"placeholder": "dd/mm/yyyy", }),
          'fast': forms.TextInput(attrs={'class': 'form-control', }),
          'fast_expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy', "placeholder": "dd/mm/yyyy", }),
          'licencia': forms.TextInput(attrs={'class': 'form-control', }),
          'licencia_expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy', "placeholder": "dd/mm/yyyy", }),
          'medico': forms.TextInput(attrs={'class': 'form-control', }),
          'medico_expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy', "placeholder": "dd/mm/yyyy", }),
      }



class Vcamion_Form(forms.ModelForm):

   class Meta:
      model = Verificacion_Camion
      fields = ['camion_id', 'verificacion', 'expira']
      widgets = {
          'camion_id': forms.TextInput(attrs={'style':'visibility:hidden; position:absolute;'}),
          'verificacion': forms.TextInput(attrs={'class': 'form-control', }),
          'expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',"placeholder": "dd/mm/yyyy", }),
      }

class Icamion_Form(forms.ModelForm):

   class Meta:
      model = Inspeccion_Camion_US
      fields = ['camion_id', 'inspeccion', 'expira']
      widgets = {
          'camion_id': forms.TextInput(attrs={'style':'visibility:hidden; position:absolute;'}),
          'inspeccion': forms.TextInput(attrs={'class': 'form-control', }),
          'expira': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',"placeholder": "dd/mm/yyyy", }),
      }

class SMXcamion_Form(forms.ModelForm):

   class Meta:
      model = Seguromx_Camion
      fields = ['camion_id', 'seguromx', 'expira_seguromx']
      widgets = {
          'camion_id': forms.TextInput(attrs={'style':'visibility:hidden; position:absolute;'}),
          'seguromx': forms.TextInput(attrs={'class': 'form-control', }),
          'expira_seguromx': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',"placeholder": "dd/mm/yyyy", }),
      }

class SUScamion_Form(forms.ModelForm):

   class Meta:
      model = Segurous_Camion
      fields = ['camion_id', 'segurous', 'expira_segurous']
      widgets = {
          'camion_id': forms.TextInput(attrs={'style':'visibility:hidden; position:absolute;'}),
          'segurous': forms.TextInput(attrs={'class': 'form-control', }),
          'expira_segurous': forms.DateInput(attrs={'class': 'form-control mydatepicker', "data-date-format": 'dd/mm/yyyy',"placeholder": "dd/mm/yyyy", }),
      }

class Repcamion_Form(forms.ModelForm):

   class Meta:
      model = Reparacion_Camion
      fields = ['camion_id','rotura','fecha_inicio','fecha_fin', 'costo_mx','costo_usd',\
                'detecto','detecto_fecha','supervisor',\
                'supervisor_fecha','autorizo','autorizo_fecha','estado']
      widgets = {
          'camion_id': forms.Select(attrs={'class':'form-control select2'}),
          'rotura': forms.TextInput(attrs={'class': 'form-control', }),
          'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',"placeholder": "dd/mm/yyyy hh:ii:ss" }),
          'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',"placeholder": "dd/mm/yyyy hh:ii:ss"}),
          'costo_usd': forms.TextInput(attrs={'class': 'form-control'}),
          'costo_mx': forms.TextInput(attrs={'class': 'form-control'}),
          'detecto': forms.Select(attrs={'class': 'form-control select2'}),
          'supervisor': forms.Select(attrs={'class': 'form-control select2'}),
          'detecto_fecha': forms.DateTimeInput(attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',"placeholder": "dd/mm/yyyy hh:ii:ss"}),
          'supervisor_fecha': forms.DateTimeInput(attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',"placeholder": "dd/mm/yyyy hh:ii:ss" }),
          'autorizo_fecha': forms.DateTimeInput(attrs={'class': 'form-control date form_datetime', "data-date-format": 'dd/mm/yyyy hh:ii:ss',"placeholder": "dd/mm/yyyy hh:ii:ss" }),

          'estado': forms.CheckboxInput(attrs={'data-on-color':"success", 'data-off-color':"info",'data-off-text':"Iniciada", 'data-on-text':"Terminada"}),
      }

class ORepcamion_Form(forms.ModelForm):

   class Meta:
      model = Orden_Reparacion_Camion
      fields = ['tipo','cantidad', 'provedor','factura',\
                'costo_r_mx','costo_r_usd','tipo_pago','descripcion']
      widgets = {
          'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
          'tipo': forms.Select(attrs={'class': 'form-control', 'required':''}),
          'cantidad': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
          'provedor': forms.TextInput(attrs={'class': 'form-control', 'required':'' }),
          'factura': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
          'costo_r_mx': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
          'costo_r_usd': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
          'tipo_pago': forms.Select(attrs={'class': 'form-control', 'required':''}),

      }



