from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from mainapp.models import News


class IndexView(TemplateView):
    template_name = "mainapp/index.html"


class ServicesView(TemplateView):
    template_name = "mainapp/services_list.html"


class NewsView(ListView):
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
