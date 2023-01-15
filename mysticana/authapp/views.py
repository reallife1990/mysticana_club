

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
# Create your views here.
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User
from random import randint


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


def generate_code():
    return str(randint(10000, 99999))

class ConfirmEmailView(TemplateView):
    template_name = 'authapp/confirm_email.html'
    extra_context = {'title': "Подтверждение email"}
    model=User
    code=''
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(context_data['view'].request.user.username)
        context_data['code'] = generate_code()
        print(context_data['code'])
        #messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')

        return context_data
    # use = HttpRequest.GET.user
    # def get(self, request,  *args, **kwargs):
    #     code = generate_code()
    #     print(request.user.email)
    #     print(code)
    #     return HttpResponse('authapp:confirm')
    # #code=generate_code()

    #send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['reallife1990msk@mail.ru'])


    def post(self, request,  *args, **kwargs):
        try:
            print(request.user.username)
            print(request.__dict__)
            if request.POST.get('conf_code') != '':
                # new_user= User.objects.create(
                #     username=request.POST.get('username'),
                #     first_name=request.POST.get('first_name'),
                #     email=request.POST.get('email')
                #     )
                # new_user.set_password(request.POST.get('password1'))
                # new_user.save()
                messages.add_message(request, messages.INFO,'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(request, messages.WARNING, 'что-то не так1')
                return HttpResponseRedirect(reverse('authapp:register'))
        except Exception as ex:
            messages.add_message(request, messages.WARNING,'что-то не так2')
            return HttpResponseRedirect(reverse('authapp:register'))

