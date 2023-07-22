from uuid import uuid4
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from datetime import datetime, date

from django.views.generic.edit import ModelFormMixin

from mainapp.models import Services, News
from .utils import DrawGraph
#@login_required
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from workplaceapp.forms import AddClientForm, ServiceChangeForm, ServiceAddForm, NewsForm, AddClientService
from workplaceapp.models import MainClients, ServiceClients

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
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        return context_data


class ShowClientView(ControlAccess, DetailView, ModelFormMixin):
    template_name = 'workplaceapp/clients_detail.html'
    model = MainClients
    form_class = AddClientService

    def get_context_data(self, **kwargs):
        self.initial ={'client': MainClients.objects.get(id=self.object.id),
                       'id': uuid4(),
                      }

        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        context_data['img'] = DrawGraph.get_plot(context_data['mainclients'].born_date,
                                                 context_data['mainclients'].age)

        return context_data

    def post(self, request, *args, **kwargs):
        form = AddClientService(self.request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.INFO, 'Консультация успешно обновлена')
            # возвращаемся на ту же страницу
            return HttpResponseRedirect(reverse_lazy('workplaceapp:client_detail',
                                                     kwargs={'pk':self.request.POST['client']}))

class AddClientView(ControlAccess,CreateView):
    model = MainClients
    template_name = 'workplaceapp/client_add.html'
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

class AllServicesView(ControlAccess, ListView):
    model = Services
    template_name = 'workplaceapp/services_list.html'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class EditServicesView(ControlAccess,UpdateView):
    model = Services
    template_name = 'workplaceapp/service_edit.html'
    form_class = ServiceChangeForm


    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        return reverse_lazy('workplaceapp:all_services')

class AddServiceView(ControlAccess,CreateView):
    model = MainClients
    template_name =  'workplaceapp/service_add.html'
    form_class = ServiceAddForm
    # success_url = reverse_lazy('workplaceapp:client_detail/', pk=)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        print(self.request.POST['pk']) # пролучили ид
        # way = self.request.POST['id']
        return reverse_lazy('mainapp:services', )
        # return reverse('workplaceapp:client_detail', pk=way)


class HistoryServicesView(ControlAccess,ListView):
    template_name = 'workplaceapp/services_history.html'
    model = ServiceClients
    paginate_by = 25


    # выборка консультаций по промежутку времени
    def get_queryset(self):
        self.kwargs['at'], self.kwargs['to'] = self.request.GET.get('dateFrom'), self.request.GET.get('dateTo')
        print(self.kwargs)
        if self.kwargs.get('at') and self.kwargs.get('to'):
            at = datetime.strptime(self.kwargs.get('at'), "%Y-%m-%d")
            to = datetime.strptime(self.kwargs.get('to'), "%Y-%m-%d")
            qs = ServiceClients.objects.filter(date__gte=at, date__lte=to).order_by('client')
            self.kwargs['period'] = f'проведённых  в период c {at.strftime("%d.%m.%Y")} ' \
                                    f'по {to.strftime("%d.%m.%Y")}'
        elif self.kwargs.get('at'):
            at = datetime.strptime(self.kwargs.get('at'), "%Y-%m-%d")
            qs=ServiceClients.objects.filter(date__gte=at).order_by('client')
            self.kwargs['period'] = f'проведённых c {at.strftime("%d.%m.%Y")}'
        elif self.kwargs.get('to'):
            to = datetime.strptime(self.kwargs.get('to'), "%Y-%m-%d")
            qs = ServiceClients.objects.filter(date__lte=to).order_by('client')
            self.kwargs['period'] = f'проведённых до {to.strftime("%d.%m.%Y")}'
        else:
            qs = ServiceClients.objects.all()
            self.kwargs['period'] = 'за весь период'
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(self.kwargs)
        context_data['period'] = f'Список консультаций {self.kwargs["period"]}'

        return context_data

class AllNewsView(ControlAccess, ListView):
    model = News
    template_name = 'workplaceapp/news_list.html'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

#Редактирование новости
class EditNewsView(ControlAccess,UpdateView):
    model = News
    template_name = 'workplaceapp/news_edit.html'
    form_class = NewsForm


    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        return reverse_lazy('workplaceapp:all_news')

#Добавление новости
class AddNewsView(ControlAccess,CreateView):
    model = News
    template_name = 'workplaceapp/news_add.html'
    form_class = NewsForm
    # success_url = reverse_lazy('workplaceapp:client_detail/', pk=)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        # print(self.request.POST['pk']) # пролучили ид
        # way = self.request.POST['id']
        return reverse_lazy('workplaceapp:all_news')

class ExpressCalcChangeView(ControlAccess,TemplateView):
    template_name = 'workplaceapp/express_calculate.html'