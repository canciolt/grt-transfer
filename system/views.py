# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from logging import Handler

from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.http import Http404
from system.forms import CamionForm, OperadorForm, Vcamion_Form, \
    Icamion_Form, Repcamion_Form, ORepcamion_Form, SMXcamion_Form
from system.models import Camion, Operador, Reparacion_Camion, Orden_Reparacion_Camion,\
    Ubicacion_Camion, Seguromx_Camion, Segurous_Camion, Verificacion_Camion, Inspeccion_Camion_US
from django.shortcuts import render, redirect
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.db import transaction


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):

    template_name = "index.html"


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


class LogoutView(RedirectView):

    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class Dinamic_Add(SuccessMessageMixin,CreateView):

    models = {"camion":Camion, "operador":Operador, "reparacion":Reparacion_Camion}
    forms ={"camion":CamionForm, "operador":OperadorForm, "reparacion":Repcamion_Form}

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.form_class = self.forms[kwargs['model']]
            self.template_name = kwargs['model']+"_form.html"
            self.success_url = "/list/"+kwargs['model']
            self.success_message = kwargs['model'] + " agregado satisfactoriamente."
        else:
            raise Http404
        return super(Dinamic_Add, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dinamic_Add, self).get_context_data(**kwargs)
        if self.model == Reparacion_Camion:
            ORepcamion = inlineformset_factory(Reparacion_Camion, Orden_Reparacion_Camion, form=ORepcamion_Form,\
                                               extra=1, can_delete=True)
            if self.request.POST:
                context['orcamion'] = ORepcamion(self.request.POST)
            else:
                context['orcamion'] = ORepcamion()
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
        return super(Dinamic_Add, self).form_valid(form)

class Dinamic_Update(SuccessMessageMixin,UpdateView):

    models = {"camion":Camion, "operador":Operador, "reparacion":Reparacion_Camion}
    forms ={"camion":CamionForm, "operador":OperadorForm, "reparacion":Repcamion_Form}


    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.form_class = self.forms[kwargs['model']]
            self.template_name = kwargs['model']+"_form.html"
            self.success_url = "/list/"+kwargs['model']
            self.success_message = kwargs['model']+" modificado satisfactoriamente."
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
                context['orcamion'] = ORepcamion(self.request.POST,instance=self.object)
            else:
                context['orcamion'] = ORepcamion(instance=self.object)
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
        return super(Dinamic_Update, self).form_valid(form)





class Dinamic_List(ListView):

    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion}

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.template_name = kwargs['model']+"_list.html"
        else:
            raise Http404
        return super(Dinamic_List, self).dispatch(request, *args, **kwargs)


class Dinamic_Delete(SuccessMessageMixin,DeleteView):

    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion}

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.success_url = "/list/"+kwargs['model']
            self.template_name = "delete.html"
            self.success_message = kwargs['model'] + " eliminado satisfactoriamente."

        else:
            raise Http404
        return super(Dinamic_Delete, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            return super(Dinamic_Delete, self).delete(request, *args, **kwargs)
        except models.ProtectedError:
            messages.add_message(request, messages.ERROR, 'Error al eliminar! dependencias protegidas')
            return redirect(self.success_url)

class Dinamic_Detail(DetailView):

    models = {"camion": Camion, "operador": Operador, "reparacion": Reparacion_Camion}

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if kwargs['model'] in self.models:
            self.model = self.models[kwargs['model']]
            self.template_name = kwargs['model']+"_detail.html"
        else:
            raise Http404
        return super(Dinamic_Detail, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(Dinamic_Detail, self).get_context_data(**kwargs)
        if self.model == Reparacion_Camion:
            orepa = Orden_Reparacion_Camion.objects.filter(id=self.object.id)
            context['orepa'] = orepa
        if self.model == Camion:
            ubi = Ubicacion_Camion.objects.filter(camion_id=self.object.id).order_by('-fecha').first()
            repa = Reparacion_Camion.objects.filter(camion_id=self.object.id)
            smx = Seguromx_Camion.objects.filter(camion_id=self.object.id).order_by('-expira_seguromx').first()
            sus = Segurous_Camion.objects.filter(camion_id=self.object.id).order_by('-expira_segurous').first()
            ins = Inspeccion_Camion_US.objects.filter(camion_id=self.object.id).order_by('-expira').first()
            ver = Verificacion_Camion.objects.filter(camion_id=self.object.id).order_by('-expira').first()
            context['repa'] = repa
            context['ubi'] = ubi
            context['si'] = {"smx":smx,"sus":sus,"ins":ins,"ver":ver}
        return context

@login_required
@csrf_protect
def Add_Exta_Camion(request,model,pk):
    forms = {"verificacion": Vcamion_Form, "inspeccion": Icamion_Form, \
             "seguromx":SMXcamion_Form, "segurous":SUScamion_Form }


    if model not in forms:
        raise Http404
    camion = Camion.objects.get(pk=pk)
    if request.method == 'POST':
        form = forms[model](request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, model+' agregado satisfactoriamente.')
            return HttpResponseRedirect('/update/camion/%s' % pk)
    else:
        form = forms[model](initial={'camion_id': pk})
    return render(request, 'vcamion_form.html', {'form': form,'camion':camion,'modelo':model})