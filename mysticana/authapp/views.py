from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login, get_user_model, logout

from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.core.exceptions import ValidationError
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm, AuthenticationForm, ChangePasswordForm
from authapp.models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from authapp.utils import send_email_for_verify
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.utils import timezone


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "authapp/login.html"
    extra_context = {'title': "Вход"}
    #messages.add_message(request, messages.INFO, 'Hello ')


class CustomLogoutView(LogoutView):
    pass


class ChangePassView(PasswordChangeView):
    template_name = 'authapp/password_change.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy("authapp:password_change_done")


class ChangeDonePassView(PasswordChangeDoneView):
    template_name = 'authapp/password_done_change.html'

    def get(self, request, *args, **kwargs): #exit
        logout(self.request)
        return super().get(self, request, args, **kwargs)


class RegisterView(View):
    model = User
    template_name = 'authapp/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            send_email_for_verify(request, user)
            text = f'На {user.email} отправлено письмо для завершения регистрации'
            messages.add_message(self.request, messages.INFO, text)
            return redirect(reverse_lazy('mainapp:index'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class CustomEditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    # success_url  для edit, update, create обязательный
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные успешно обновлены')
        return reverse_lazy('authapp:edit', args=[self.request.user.id])

    def get_object(self, queryset=None):  # ограничение на редактирование только своего профиля
        return self.request.user


class VerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.confirm_email = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('mainapp:index')) # если ок
        text = f'Ссылка-подтверждения устарела или неверна. Авторизируйтесь снова для получения актульной ссылки'
        messages.add_message(self.request, messages.WARNING, text)
        return HttpResponseRedirect(reverse('authapp:login')) # если хуй

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
