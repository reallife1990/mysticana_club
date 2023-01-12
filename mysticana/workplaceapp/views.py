from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from datetime import datetime
class MainView(TemplateView):
    template_name = 'workplaceapp/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['date_now']= datetime.now()
        return context_data