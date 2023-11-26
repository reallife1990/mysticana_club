from uuid import uuid4
from django.core.paginator import Paginator
from django.db.models import Count, Q, F, Subquery
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from datetime import datetime, date

from django.views.generic.edit import ModelFormMixin

from mainapp.models import Services, News
from .utils import DrawGraph, Calculate, TablePifagora
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
    paginate_by = 5

    @staticmethod
    def get_text_sort(params):
        lst = list(params.split('&')[1:])
        # print(len(lst))
        types = {'types':'Сортировка:', 'sort':' ','serv': 'Консультации', 'reg': 'Дата регистрации', 'born': 'Дата рождения',
        'up':'( по возрастанию)', 'down':'( по убыванию)','ageAt':'C ', 'ageTo':' по ', 'search':' Выборка по тексту:'}

        filter_text = ''
        if len(lst) > 0:
            d = {}
            for i in lst:
                d[i.split('=')[0]] = i.split('=')[1]
            print(d)
            for k,v in d.items():
                print(k,v)
                if k in ['ageAt']:
                    filter_text+='Выборка по годам рождения '
                if types.get(k) and v !='':
                    print(k)
                    filter_text+=types.get(k)
                    if types.get(v):
                        filter_text+=types.get(v)
                    else:
                        filter_text+= v
                else:
                    print('notfound')
        # print(filter_text)
        return filter_text


    # ф-ция сохранения сортировки
    def get_filter_params(self):
        params = ''
        for k, v in dict(self.request.GET).items():
            if k != 'page':
                params = params + f'&{k}={v[0]}'
        # print(params)
        self.get_text_sort(params)
        return params

    def get_queryset(self):
        lst = dict(self.request.GET).keys()
        # сортировка выбором
        if self.request.GET.get('sort'):
            p = '-' if self.request.GET.get('sort') == 'down' else ''
            if self.request.GET.get('types') == 'reg':
                qs = MainClients.objects.order_by(f'{p}date_created')
            elif self.request.GET.get('types') == 'born':
                qs = MainClients.objects.order_by(f'{p}born_date')
            elif self.request.GET.get('types') == 'serv':
                qs = MainClients.objects.annotate(sc=Count('client_of')).order_by(f'{p}sc')
            # print(so,ty)
        # по части имени фамилии
        elif self.request.GET.get('search'):
            qs = MainClients.objects.filter(Q(first_name__contains=self.request.GET.get('search')) |
                                            Q(last_name__contains=self.request.GET.get('search')))
        # сортировка по году рождения
        elif self.request.GET.get('ageAt') or self.request.GET.get('ageTo'):
            if self.request.GET.get('ageAt') and not self.request.GET.get('ageTo'):
                qs = MainClients.objects.filter(born_date__year__gte=self.request.GET.get('ageAt'))
            elif self.request.GET.get('ageTo') and not self.request.GET.get('ageAt'):
                qs = MainClients.objects.filter(born_date__year__lte=self.request.GET.get('ageTo'))
            else:
                qs = MainClients.objects.filter(Q(born_date__year__gte=self.request.GET.get('ageAt')) &
                                                Q(born_date__year__lte=self.request.GET.get('ageTo')))
        else:
            qs = MainClients.objects.order_by('-photo')
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        context_data['sort_list'] = self.get_filter_params()
        context_data['filter_text'] = self.get_text_sort(self.get_filter_params())

        return context_data


class ShowClientView(ControlAccess, DetailView, ModelFormMixin):
    template_name = 'workplaceapp/clients_detail.html'
    model = MainClients
    form_class = AddClientService

    def get_context_data(self, **kwargs):
        self.initial ={'client': MainClients.objects.get(id=self.object.id),'id': uuid4(),}

        context_data = super().get_context_data(**kwargs)
        context_data['date_now'] = datetime.now()
        context_data['img'] = DrawGraph.get_plot(context_data['mainclients'].born_date,
                                                 context_data['mainclients'].age)
        return context_data

    def post(self, request, *args, **kwargs):
        form = AddClientService(self.request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            r=messages.INFO
            txt='Консультация успешно обновлена'
            # messages.add_message(self.request, messages.INFO, 'Консультация успешно обновлена')
            # # возвращаемся на ту же страницу
            # return HttpResponseRedirect(reverse_lazy('workplaceapp:client_detail',
            #                                          kwargs={'pk' : self.request.POST['client']}))
        else:
            form.clean()
            r=messages.ERROR
            txt="ошибка"
        messages.add_message(self.request, r, txt)
        return HttpResponseRedirect(reverse_lazy('workplaceapp:client_detail',
                                                 kwargs={'pk': self.request.POST['client']}))

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
    template_name ='workplaceapp/service_add.html'
    form_class = ServiceAddForm
    # success_url = reverse_lazy('workplaceapp:client_detail/', pk=)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        return reverse_lazy('mainapp:services', )
        # return reverse('workplaceapp:client_detail', pk=way)


class HistoryServicesView(ControlAccess,ListView):
    template_name = 'workplaceapp/services_history.html'
    model = ServiceClients
    paginate_by = 25


    # выборка консультаций по промежутку времени
    def get_queryset(self):
        self.kwargs['at'], self.kwargs['to'] = self.request.GET.get('dateFrom'), self.request.GET.get('dateTo')
        # print(self.kwargs)
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
        # print(self.kwargs)
        context_data['period'] = f'Список консультаций {self.kwargs["period"]}'

        return context_data

#Все новости
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
        return reverse_lazy('workplaceapp:all_news')


#Экспресс расчёт выбор
class ExpressCalcChangeView(ControlAccess,TemplateView):
    template_name = 'workplaceapp/express_calculate.html'

    def get_queryset(self):
        # self.kwargs['at'], self.kwargs['to'] = self.request.GET.get('dateFrom'), self.request.GET.get('dateTo')
        print(self.request.GET)

    def get_context_data(self, **kwargs):
        # print(self.request.GET)
        context_data = super().get_context_data(**kwargs)
        # context_data['date'] = self.request.GET.get('datein')
        if (self.request.GET.get('txt')):
            context_data['result']=Calculate.words_in_number(self.request.GET.get('txt'))
            context_data['txt'] = self.request.GET.get('txt')
            # print(context_data)
        return context_data

# экспресс расчёт
class ExpressCalcResultView(ControlAccess,TemplateView):
    template_name = 'workplaceapp/express_result.html'

    def get_queryset(self):
        # self.kwargs['at'], self.kwargs['to'] = self.request.GET.get('dateFrom'), self.request.GET.get('dateTo')
        print(self.kwargs.__dict__)
    def get_context_data(self, **kwargs):
        # print(self.request.GET)
        context_data = super().get_context_data(**kwargs)
        context_data['date'] = self.request.GET.get('datein')
        print(self.request.GET)
        date_for = datetime.strptime(self.request.GET.get('datein'), "%Y-%m-%d")
        #график
        if self.request.GET.get('scale'):
            context_data['img'] = DrawGraph.get_plot(date_for, Calculate.age(date_for))
        if self.request.GET.get('vid'):
            context_data['main_tbl']=Calculate.main_table(date_for, Calculate.age(date_for))
        if self.request.GET.get('matrix'):
            context_data['work_numbers'] = TablePifagora.work_numbers(date_for)
            context_data['pifagor'] = TablePifagora.data_answer(date_for)
        if self.request.GET.get('way'):
            context_data['way'] = Calculate.karm_way(date_for)
        # print(Calculate.words_in_number('12'))
        return context_data

