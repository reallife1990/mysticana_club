from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from datetime import datetime

#@login_required
from mysticana import settings
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect


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