from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render


from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView

from authapp.models import User
from mainapp.forms import NewClientForm

from mainapp.models import News, Services
from workplaceapp.models import ServiceClients, MainClients


class ControlAccess(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            return self.handle_no_permission()
        else:
            print(request.user.client.born_date)
        if not self.request.user.is_superuser:
            # Redirect the user to somewhere else - add your URL here
            # переадресация если не суперюзер
            return HttpResponseRedirect('/')

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)

class IndexView(TemplateView):
    template_name = "mainapp/index.html"


class ServicesView(ListView):
    #  отображение услуг
    template_name = "mainapp/services_list.html"
    model = Services
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class ServiceDetailView(ControlAccess, TemplateView):
    '''просмотр услуги'''
    template_name = 'mainapp/service_detail.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        query = Services.objects.filter(deleted=False)
        next = query.filter(pk__gt=self.kwargs.get('pk')).values('pk', 'title').first()
        prev = query.filter(pk__lt=self.kwargs.get('pk')).reverse().values('pk','title').first()
        context_data['object'] = get_object_or_404(Services, pk=self.kwargs.get('pk'))
        if prev is None :
            prev = query.values('pk', 'title').last()
        if next is None:
            next = query.values('pk', 'title').first()
        context_data['next'] = next
        context_data['prev'] = prev
        context_data['count'] = ServiceClients.objects.filter(service__pk=self.kwargs.get('pk')).count()

        return context_data


class NewsView(ListView):
    '''новости'''
    template_name = "mainapp/news.html"
    model = News
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['object_list'] = News.objects.filter(deleted=False)
    #
    #     return context_data


class NewsDetailView(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = get_object_or_404(News, pk=self.kwargs.get('pk'))

        return context_data


class AddProfileView(CreateView):
    '''стать клиентом'''
    template_name = 'mainapp/get_profile.html'
    model = MainClients
    form_class = NewClientForm

    def get_initial(self):
        """
        автозролнение обязательных пользовательских полей
        :return:
        """
        initial = super().get_initial()
        initial['first_name'] =self.request.user.first_name#User.objects.get(id=self.kwargs['article_id'])
        initial['last_name'] =self.request.user.last_name
        initial['user'] = self.request.user
        print(self.request.user)
        return initial
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['first_name'] =self.request.user.first_name

        return context_data

    def get_success_url(self):
        self.change_client_status()
        messages.add_message(self.request, messages.SUCCESS, 'Поздравляем! Вы стали клиентом!')
        return reverse_lazy('mainapp:index')

    def change_client_status(self):
        user = User.objects.get(id=self.request.user.id)
        user.is_client = True
        user.save()





class EditProfileView(UpdateView):
    '''стать клиентом'''
    template_name = 'mainapp/get_profile.html'
    model = MainClients
    form_class = NewClientForm


    def get_object(self, queryset=None):
        print(self.kwargs.get('pk')) # ограничение на редактирование только своего профиля
        res=MainClients.objects.get(user_id=self.kwargs.get('pk'))
        print(res.pk)
        return MainClients.objects.get(id=res.pk)
        # return self.request.user

    # def get_queryset(self):
    #     return super().get_queryset().get(user_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)