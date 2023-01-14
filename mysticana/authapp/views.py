from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
# Create your views here.
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


class CustomLoginView(LoginView):
    template_name = "authapp/login.html"
    extra_context = {'title': "Вход"}



class CustomLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy('mainapp:index')


class CustomEditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    # success_url  для edit, update, create обязательный
    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.id])

    def get_object(self, queryset=None):  # ограничение на редактирование только своего профиля
        return self.request.user


# class RegisterView(TemplateView):
#     template_name = "authapp/register.html"
#     extra_context = {'title':"Регистрация"}
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if all(
#                     (request.POST.get('username'),
#                     request.POST.get('email'),
#                     request.POST.get('first_name'),
#                     request.POST.get('password1') == request.POST.get('password2')
#                     )
#             ):
#                 new_user= User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     email=request.POST.get('email')
#                     )
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO,'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#             else:
#                 messages.add_message(request, messages.WARNING, 'что-то не так1')
#                 return HttpResponseRedirect(reverse('authapp:register'))
#         except Exception as ex:
#             messages.add_message(request, messages.WARNING,'что-то не так2')
#             return HttpResponseRedirect(reverse('authapp:register'))
#
#



class EditView(TemplateView):
    pass