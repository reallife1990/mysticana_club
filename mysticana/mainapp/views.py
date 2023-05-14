from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from mainapp.models import News, Services
from workplaceapp.models import ServiceClients


class IndexView(TemplateView):
    template_name = "mainapp/index.html"


class ServicesView(ListView):
    #  отображение услуг
    template_name = "mainapp/services_list.html"
    model = Services
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class ServiceDetailView(TemplateView):
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
