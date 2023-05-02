from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView
# Create your views here.
from datetime import datetime, date
from .utils import DrawGraph
#@login_required
from mysticana import settings
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from workplaceapp.forms import AddClientForm
from workplaceapp.models import MainClients


class ControlAccess(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            # переадресация если не авторизованы
            return self.handle_no_permission()
        if not self.request.user.is_superuser:
            # Redirect the user to somewhere else - add your URL here
            # переадресация если не суперюзер
            return HttpResponseRedirect('/')

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class MainView(ControlAccess, TemplateView):
    template_name = 'workplaceapp/index.html'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        return context_data

class ShowAllClientsView(ControlAccess,ListView):
    template_name = 'workplaceapp/clients_list.html'
    model = MainClients

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        return context_data


class ShowClientView(ControlAccess, DetailView):
    template_name = 'workplaceapp/clients_detail.html'
    model = MainClients

    #print(MainClients.object.born_date)
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        print (context_data['mainclients'].born_date)
        context_data['img'] = DrawGraph.get_plot(context_data['mainclients'].born_date,
                                                 context_data['mainclients'].age)
        return context_data

class AddClientView(ControlAccess,CreateView):
    model = MainClients
    template_name =  'workplaceapp/client_add.html'
    form_class = AddClientForm
    # success_url = reverse_lazy('workplaceapp:client_detail/', pk=)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        print(self.request.POST['id']) # пролучили ид
        way = self.request.POST['id']
        return reverse_lazy('workplaceapp:client_detail', kwargs={'pk': way})
        # return reverse('workplaceapp:client_detail', pk=way)

    # { % url
    # 'workplaceapp:client_detail'
    # pk = client.pk %}