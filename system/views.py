# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, FormView
from django.http import Http404
from system.forms import *
from system.models import *
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        operaciones = Operacion.objects.filter(estado="T")
        op = Operacion.objects.all()
        imp = 0
        exp = 0
        cancel = 0
        proc = 0
        for o in op:
            if o.estado == 'C':
                cancel += 1
            if o.estado == 'I':
                proc += 1

        for o in operaciones:
            try:
                if o.servicio.servicio_cruce:
                    if o.servicio.servicio_cruce == "IMP" or o.servicio.servicio_cruce == "IMPV":
                        imp += 1
                    if o.servicio.servicio_cruce == "EXP" or o.servicio.servicio_cruce == "EXPV":
                        exp += 1

            except ObjectDoesNotExist:
                pass
        clientes = Cliente.objects.all().order_by('-id')[0:5]

        context['importacion'] = imp
        context['exportacion'] = exp
        context['proceso'] = proc
        context['cancelada'] = cancel
        context['clientes'] = clientes

        return context



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect("/")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get("next"):
            redirect_to = self.request.GET.get("next")
        else:
            redirect_to = "/"
        return redirect_to


class Dinamic_Add(SuccessMessageMixin, CreateView):
    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion, \
              "cliente": Cliente, "consignatario": Consignatario, "patio": Patio, "servicio": Servicio_Cruce, \
              "servicio_ext": Servicio_Extra, "caja": Caja, "operacion": Operacion, "factura": Factura}
    forms = {"camion": CamionForm, "operador": OperadorForm, "reparacion": Repcamion_Form, \
             "cliente": Cliente_Form, "consignatario": Consignatario_Form, "patio": Patio_Form, \
             "servicio": Servicio_Cruce_Form, "servicio_ext": Servicio_Extra_Form, "caja": Caja_Form, \
             "operacion": Operacion_Form, "factura": Factura_Form}

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.form_class = self.forms[kwargs['model']]
            self.template_name = kwargs['model'] + "_form.html"
            if self.model == Servicio_Extra or self.model == Servicio_Cruce:
                self.success_url = "/list/servicio"
            else:
                self.success_url = "/list/" + kwargs['model']
            self.success_message = kwargs['model'] + " agregado satisfactoriamente."
        else:
            raise Http404
        return super(Dinamic_Add, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dinamic_Add, self).get_context_data(**kwargs)
        if self.model == Reparacion_Camion:
            ORepcamion = inlineformset_factory(Reparacion_Camion, Orden_Reparacion_Camion, form=ORepcamion_Form, \
                                               extra=1, can_delete=True)
            if self.request.POST:
                context['orcamion'] = ORepcamion(self.request.POST)
            else:
                context['orcamion'] = ORepcamion()
        if self.model == Cliente:
            CCliente = inlineformset_factory(Cliente, Contactos_Cliente, form=Contacto_Cliente_Form, \
                                             extra=1, can_delete=True)
            DCliente = inlineformset_factory(Cliente, Despachador_Cliente, form=Despachador_Cliente_Form, \
                                             extra=1, can_delete=True)
            if self.request.POST:
                context['ccliente'] = CCliente(self.request.POST)
                context['dcliente'] = DCliente(self.request.POST)
                context['usuarioform'] = Resgistro_User_Cliente_Form(self.request.POST)
            else:
                context['ccliente'] = CCliente()
                context['dcliente'] = DCliente()
                context['usuarioform'] = Resgistro_User_Cliente_Form()
        if self.model == Consignatario:
            try:
                context['cliente'] = get_object_or_404(Cliente, pk=self.kwargs['pk'])
                EConsignatario = inlineformset_factory(Consignatario, Ejecutivo_Consignatario,
                                                       form=Ejecutivo_Consignatario_Form, \
                                                       extra=1, can_delete=True)
                if self.request.POST:
                    context['econsignatario'] = EConsignatario(self.request.POST)
                    context['usuarioform'] = Resgistro_User_Cliente_Form(self.request.POST)
                else:
                    context['econsignatario'] = EConsignatario()
                    context['usuarioform'] = Resgistro_User_Cliente_Form()
            except KeyError:
                raise Http404
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if self.model == Reparacion_Camion:
            orcamion = context['orcamion']
            with transaction.atomic():
                self.object = form.save(commit=False)
                if orcamion.is_valid():
                    self.object.save()
                    orcamion.instance = self.object
                    orcamion.save()
                else:
                    return super(Dinamic_Add, self).form_invalid(form)
        if self.model == Cliente:
            usuario = context['usuarioform']
            ccliente = context['ccliente']
            dcliente = context['dcliente']
            with transaction.atomic():
                if ccliente.is_valid() and dcliente.is_valid():
                    if usuario.is_valid():
                        user = User.objects.create_user(
                            username=usuario.cleaned_data['username'],
                            password=usuario.cleaned_data['password1'],
                            email=usuario.cleaned_data['email'])
                        user.first_name = usuario.cleaned_data['first_name']
                        user.is_active = usuario.cleaned_data['is_active']
                        user.save()
                        cliente = form.save(commit=False)
                        cliente.usuario = user
                        cliente.save()
                        ccliente.instance = cliente
                        ccliente.save()
                        dcliente.instance = cliente
                        dcliente.save()
                        return HttpResponseRedirect('/list/cliente')
                    else:
                        return super(Dinamic_Add, self).form_invalid(form)
                else:
                    return super(Dinamic_Add, self).form_invalid(form)
        if self.model == Consignatario:
            usuario = context['usuarioform']
            econsignatario = context['econsignatario']
            with transaction.atomic():
                if econsignatario.is_valid():
                    if usuario.is_valid():
                        user = User.objects.create_user(
                            username=usuario.cleaned_data['username'],
                            password=usuario.cleaned_data['password1'],
                            email=usuario.cleaned_data['email'])
                        user.first_name = usuario.cleaned_data['first_name']
                        user.is_active = usuario.cleaned_data['is_active']
                        user.save()
                        consignatario = form.save(commit=False)
                        consignatario.usuario = user
                        consignatario.save()
                        econsignatario.instance = consignatario
                        econsignatario.save()
                        return HttpResponseRedirect('/list/cliente')
                    else:
                        return super(Dinamic_Add, self).form_invalid(form)
                else:
                    return super(Dinamic_Add, self).form_invalid(form)
        if self.model == Operador:
            camion = get_object_or_404(Camion, pk=form.cleaned_data['camion'].id)
            with transaction.atomic():
                camion.estado = 1
                camion.save()
        if self.model == Operacion:
            s = form.cleaned_data['sello']
            operador = form.cleaned_data['operador']
            caja = form.cleaned_data['caja']
            with transaction.atomic():
                operacion = form.save()
                ope = get_object_or_404(Operador, pk=operador.id)
                ope.estado = True
                ope.save()
                ca = get_object_or_404(Caja, pk=caja.id)
                ca.estado = True
                ca.save()
                sello = Sello_Operacion()
                sello.operacion = operacion
                sello.sello = s
                sello.fecha = datetime.now()
                sello.observaciones = "Sello de salida"
                sello.save()
                event = Evento_Operacion(evento="INIT", operacion=operacion, fecha_inicio=operacion.fecha_inicio)
                event.save()
        return super(Dinamic_Add, self).form_valid(form)


class Dinamic_Update(SuccessMessageMixin, UpdateView):
    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion, \
              "usuario": User, "cliente": Cliente, "consignatario": Consignatario, "patio": Patio, \
              "servicio": Servicio_Cruce, "servicio_ext": Servicio_Extra, "caja": Caja, "operacion": Operacion}
    forms = {"camion": CamionForm, "operador": OperadorForm, "reparacion": Repcamion_Form, \
             "usuario": User_Form, "cliente": Cliente_Form, "consignatario": Consignatario_Form, \
             "patio": Patio_Form, "servicio": Servicio_Cruce_Form, "servicio_ext": Servicio_Extra_Form, \
             "caja": Caja_Form, "operacion": Operacion_Form}

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.form_class = self.forms[kwargs['model']]
            self.template_name = kwargs['model'] + "_form.html"
            if self.model == Servicio_Extra or self.model == Servicio_Cruce:
                self.success_url = "/list/servicio"
            else:
                self.success_url = "/list/" + kwargs['model']
            self.success_message = kwargs['model'] + " modificado satisfactoriamente."
        else:
            raise Http404
        return super(Dinamic_Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dinamic_Update, self).get_context_data(**kwargs)
        context['accion'] = 'update'
        if self.model == Reparacion_Camion:
            ORepcamion = inlineformset_factory(Reparacion_Camion, Orden_Reparacion_Camion, form=ORepcamion_Form, \
                                               extra=0, can_delete=True)
            if self.request.POST:
                context['orcamion'] = ORepcamion(self.request.POST, instance=self.object)
            else:
                context['orcamion'] = ORepcamion(instance=self.object)
        if self.model == Cliente:
            CCliente = inlineformset_factory(Cliente, Contactos_Cliente, form=Contacto_Cliente_Form, \
                                             extra=0, can_delete=True)
            DCliente = inlineformset_factory(Cliente, Despachador_Cliente, form=Despachador_Cliente_Form, \
                                             extra=0, can_delete=True)
            if self.request.POST:
                context['ccliente'] = CCliente(self.request.POST, instance=self.object)
                context['dcliente'] = DCliente(self.request.POST, instance=self.object)
            else:
                context['ccliente'] = CCliente(instance=self.object)
                context['dcliente'] = DCliente(instance=self.object)
        if self.model == Consignatario:
            context['cliente'] = get_object_or_404(Cliente, pk=self.object.cliente.id)
            EConsignatario = inlineformset_factory(Consignatario, Ejecutivo_Consignatario,
                                                   form=Ejecutivo_Consignatario_Form, \
                                                   extra=0, can_delete=True)
            if self.request.POST:
                context['econsignatario'] = EConsignatario(self.request.POST, instance=self.object)
            else:
                context['econsignatario'] = EConsignatario(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if self.model == Reparacion_Camion:
            orcamion = context['orcamion']
            with transaction.atomic():
                if orcamion.is_valid():
                    orcamion.save()
                else:
                    return super(Dinamic_Update, self).form_invalid(form)
        if self.model == Cliente:
            ccliente = context['ccliente']
            dcliente = context['dcliente']
            with transaction.atomic():
                if ccliente.is_valid() and dcliente.is_valid():
                    ccliente.save()
                    dcliente.save()
                else:
                    return super(Dinamic_Update, self).form_invalid(form)
        if self.model == Consignatario:
            EConsignatario = context['econsignatario']
            with transaction.atomic():
                if EConsignatario.is_valid():
                    EConsignatario.save()
                    self.success_url = "/detail/cliente/" + str(self.object.cliente.id)
                else:
                    return super(Dinamic_Update, self).form_invalid(form)
        if self.model == Operador:
            operador = get_object_or_404(Operador, pk=self.object.id)
            camion = get_object_or_404(Camion, pk=form.cleaned_data['camion'].id)
            with transaction.atomic():
                operador.camion.estado = 0
                operador.camion.save()
                camion.estado = 1
                camion.save()
        # Pendiente update Operacion -------
        if self.model == Operacion:
            sello = Sello_Operacion.objects.filter(sello=form.cleaned_data['sello']).count()
            operador = get_object_or_404(Operador, pk=form.cleaned_data['operador'].id)
            caja = get_object_or_404(Caja, pk=form.cleaned_data['caja'].id)
            operacion = get_object_or_404(Operacion, pk=self.object.id)
            with transaction.atomic():
                operacion.operador.estado = False
                operacion.operador.save()
                operador.estado = True
                operador.save()
                operacion.caja.estado = False
                operacion.caja.save()
                caja.estado = True
                caja.save()
                if sello == 0:
                    s = Sello_Operacion()
                    s.operacion = operacion
                    s.sello = form.cleaned_data['sello']
                    s.fecha = datetime.now()
                    s.observaciones = "Sello de salida"
                    s.save()
        return super(Dinamic_Update, self).form_valid(form)


class Dinamic_List(ListView):
    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion, \
              "usuario": User, "cliente": Cliente, "patio": Patio, "servicio": Servicio, "operacion": Operacion, \
              "caja": Caja, "oppendientes": Operacion, "factura": Factura, "facturaspagadas": Factura, \
              "facturascanceladas": Factura, "opterminadas": Operacion, "opcanceladas": Operacion}
    pk_model = ""

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.pk_model = kwargs['model']
            self.template_name = kwargs['model'] + "_list.html"
        else:
            raise Http404
        return super(Dinamic_List, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dinamic_List, self).get_context_data(**kwargs)
        context['accion'] = 'update'
        if self.model == Servicio:
            context['cruce'] = Servicio_Cruce.objects.all()
            context['extra'] = Servicio_Extra.objects.all()
        return context

    def get_queryset(self):
        queryset = super(Dinamic_List, self).get_queryset()
        if self.model == Operacion and (self.pk_model != "oppendientes" and self.pk_model != "opterminadas" and self.pk_model != "opcanceladas"):
            return queryset.filter(estado="I")
        if self.pk_model == "oppendientes":
            return queryset.filter(estado="P")
        if self.pk_model == "opterminadas":
            return queryset.filter(estado="T")
        if self.pk_model == "opcanceladas":
            return queryset.filter(estado="C")
        if self.model == Factura and (self.pk_model != "facturaspagadas" and self.pk_model != "facturascanceladas") :
            return queryset.filter(estado='A').order_by('fecha')
        if self.pk_model == "facturaspagadas":
            return queryset.filter(estado='P').order_by('fecha')
        if self.pk_model == "facturascanceladas":
            return queryset.filter(estado='C').order_by('fecha')
        return queryset


class Dinamic_Delete(SuccessMessageMixin, DeleteView):
    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion, \
              "usuario": User, "cliente": Cliente, "consignatario": Consignatario, "patio": Patio, \
              "servicio": Servicio_Cruce, "servicio_ext": Servicio_Extra, "caja": Caja, "operacion": Operacion, \
              "payment": Pagos}

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            if self.models == Servicio_Extra or self.model == Servicio_Cruce:
                self.success_url = "/list/servicio"
            else:
                self.success_url = "/list/" + kwargs['model']
            self.template_name = "delete.html"
            self.success_message = kwargs['model'] + " eliminado satisfactoriamente."

        else:
            raise Http404
        return super(Dinamic_Delete, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.model == Consignatario:
            cliente = get_object_or_404(Consignatario, pk=kwargs['pk']).cliente
            self.success_url = "/detail/cliente/" + str(cliente.id)
        try:
            if self.model == Operador:
                operador = get_object_or_404(Operador, pk=kwargs['pk'])
                operador.camion.estado = 0
                operador.camion.save()
            if self.model == Operacion:
                operacion = get_object_or_404(Operacion, pk=kwargs['pk'])
                if operacion.estado == 'P':
                    eventoop = Evento_Operacion.objects.filter(operacion=operacion)
                    conceptoop = Concepto_Operacion.objects.filter(operacion=operacion)
                    selloop = Sello_Operacion.objects.filter(operacion=operacion)
                    with transaction.atomic():
                        for e in eventoop:
                            e.delete()
                        for c in conceptoop:
                            c.delete()
                        for s in selloop:
                            s.delete()
                        ope = get_object_or_404(Operador, pk=operacion.operador.id)
                        ope.estado = False
                        ope.save()
                        ca = get_object_or_404(Caja, pk=operacion.caja.id)
                        ca.estado = False
                        ca.save()
                else:
                    messages.add_message(request, messages.ERROR, 'Solo se pueden eliminar operaciones pendientes !')
                    return redirect(self.success_url)
            if self.model == Pagos:
                payment = get_object_or_404(Pagos, pk=kwargs['pk'])
                self.success_url = "/payments"
                if payment.estado != 'P':
                    messages.add_message(request, messages.ERROR, 'Solo se pueden eliminar pagos pendientes aprobación !')
                    return redirect(self.success_url)
            return super(Dinamic_Delete, self).delete(request, *args, **kwargs)
        except models.ProtectedError:
            messages.add_message(request, messages.ERROR, 'Error al eliminar! dependencias protegidas')
            return redirect(self.success_url)


class Dinamic_Detail(DetailView):
    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion, \
              "cliente": Cliente, "patio": Patio, "servicio": Servicio_Cruce, "servicio_ext": Servicio_Extra, \
              "caja": Caja, "operacion": Operacion, "factura": Factura}

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.template_name = kwargs['model'] + "_detail.html"
        else:
            raise Http404
        return super(Dinamic_Detail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dinamic_Detail, self).get_context_data(**kwargs)
        if self.model == Reparacion_Camion:
            orepa = Orden_Reparacion_Camion.objects.filter(id=self.object.id)
            context['orepa'] = orepa
        if self.model == Cliente:
            ccliente = Contactos_Cliente.objects.filter(cliente=self.object.id)
            consignatarios = Consignatario.objects.filter(cliente=self.object.id, usuario__is_active=True)
            despachadores = Despachador_Cliente.objects.filter(cliente=self.object.id)
            context['ccliente'] = ccliente
            context['consignatarios'] = consignatarios
            context['despachadores'] = despachadores
        if self.model == Camion:
            ubi = Ubicacion_Camion.objects.filter(camion_id=self.object.id).order_by('-fecha').first()
            repa = Reparacion_Camion.objects.filter(camion_id=self.object.id)
            smx = Seguromx_Camion.objects.filter(camion_id=self.object.id).order_by('-expira_seguromx').first()
            sus = Segurous_Camion.objects.filter(camion_id=self.object.id).order_by('-expira_segurous').first()
            ins = Inspeccion_Camion_US.objects.filter(camion_id=self.object.id).order_by('-expira').first()
            ver = Verificacion_Camion.objects.filter(camion_id=self.object.id).order_by('-expira').first()
            context['repa'] = repa
            context['ubi'] = ubi
            context['si'] = {"smx": smx, "sus": sus, "ins": ins, "ver": ver}
        if self.model == Operacion:
            sellos = Sello_Operacion.objects.filter(operacion=self.object.id).order_by('-fecha')[:1]
            eventos = Evento_Operacion.objects.filter(operacion=self.object.id).order_by('id')
            conceptos = Concepto_Operacion.objects.filter(operacion=self.object.id).order_by('fecha_concepto')
            context['sellos'] = sellos
            context['eventos'] = eventos
            context['conceptos'] = conceptos
            context['form_sello'] = Sellos_Form(initial={"operacion": self.object.id})
            context['form_evento'] = Evento_Form(initial={"operacion": self.object.id})
            context['form_concepto'] = Concepto_Form(initial={"operacion": self.object.id})
        if self.model == Factura:
            opera = Factura_Operacion.objects.filter(factura=self.object.id)
            operaciones = []
            iva = 0
            subtotalmx = 0
            subtotalusd = 0
            totalmx = 0
            totalusd = 0
            for o in opera:
                conc_operacion = Concepto_Operacion.objects.filter(operacion=o.operacion.id).order_by('fecha_concepto')
                imp_usd = o.operacion.servicio.importeusd
                imp_mxn = o.operacion.servicio.importemx
                subtotalmx += imp_mxn
                subtotalusd += imp_usd
                if o.operacion.servicio.iva == True:
                    iva += imp_mxn * 0.16
                for conc in conc_operacion:
                    subtotalusd += conc.costo_usd
                    subtotalmx += conc.costo_mx
                    if o.operacion.servicio.iva == True:
                        iva += conc.costo_mx * 0.16
                operaciones.append(
                    {"id": o.operacion.id, "fecha": o.operacion.fecha_inicio, "servicio": o.operacion.servicio, \
                     "consignatario": o.operacion.consignatario, "importeusd": imp_usd,
                     "importemxn": imp_mxn,
                     "conceptos": conc_operacion})
            totalmx += subtotalmx + iva
            totalusd += subtotalusd
            extra = {"subtotalusd": subtotalusd, "totalusd": totalusd, "subtotalmx": subtotalmx, "totalmx": totalmx,
                     "iva": iva}
            context['operaciones'] = operaciones
            context['extra'] = extra
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class Registro_View(SuccessMessageMixin, FormView):
    template_name = 'usuario_form.html'
    form_class = Resgistro_Form
    success_url = '/list/usuario'
    success_message = 'El usuario se agrego satisfactoriamente'

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )
        return super(Registro_View, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class Password_View(SuccessMessageMixin, FormView):
    template_name = 'usuario_form.html'
    form_class = EditPasswordForm
    success_url = '/list/usuario'
    success_message = 'La contraseña se cambio satisfactoriamente'

    def get_form_kwargs(self):
        kwargs = super(Password_View, self).get_form_kwargs()
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Password_View, self).get_context_data(**kwargs)
        context['accion'] = 'passwd'
        return context


@login_required
@staff_member_required
@csrf_protect
def Add_Exta_Camion(request, model, pk):
    forms = {"verificacion": Vcamion_Form, "inspeccion": Icamion_Form, \
             "seguromx": SMXcamion_Form, "segurous": SUScamion_Form}
    if model not in forms:
        raise Http404
    camion = Camion.objects.get(pk=pk)
    if request.method == 'POST':
        form = forms[model](request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, model + ' agregado satisfactoriamente.')
            return HttpResponseRedirect('/update/camion/%s' % pk)
    else:
        form = forms[model](initial={'camion_id': pk})
    return render(request, 'vcamion_form.html', {'form': form, 'camion': camion, 'modelo': model})


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PagosView(TemplateView):
    template_name = "payments.html"

    def get_context_data(self, **kwargs):
        context = super(PagosView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.filter(usuario__is_active=True).order_by('id')
        context['pagos_pendientes'] = Pagos.objects.filter(estado='P')
        context['form_payment'] = Pagos_Form()
        return context


@login_required
def get_tasa_cambio(request):
    try:
        from suds.client import Client
        from xml.dom import minidom
        choice = dict()
        banxico = Client("http://www.banxico.org.mx:80/DgieWSWeb/DgieWS?WSDL")
        banxico_request = banxico.service.tiposDeCambioBanxico()
        xmldoc = minidom.parseString(banxico_request.format(str).encode('utf-8'))
        itemlist = xmldoc.getElementsByTagName('bm:Series')
        for s in itemlist:
            if s.attributes['IDSERIE'].value == 'SF60653':
                itemlist2 = s.getElementsByTagName('bm:Obs')
                choice['fecha'] = itemlist2[0].attributes['TIME_PERIOD'].value
                choice['tasa'] = itemlist2[0].attributes['OBS_VALUE'].value
        return choice
    except:
        return False
