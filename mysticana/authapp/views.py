from django.views.generic import TemplateView
# Create your views here.


class LoginView(TemplateView):
    template_name = "authapp/login.html"
    extra_context = {'title': "Вход"}



class LogoutView(TemplateView):
    pass


class RegisterView(TemplateView):
    template_name = "authapp/register.html"
    extra_context = {'title':"Регистрация"}


class EditView(TemplateView):
    pass