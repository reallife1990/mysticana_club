from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.core.exceptions import ValidationError
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm, AuthenticationForm
from authapp.models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from authapp.utils import send_email_for_verify
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "authapp/login.html"
    extra_context = {'title': "Вход"}

class CustomLogoutView(LogoutView):
    pass


# class RegisterView(CreateView):
#     model = User
#     form_class = CustomUserCreationForm
#     template_name = "authapp/register.html"
#
#     # переадресовать что б проверили почту
#     success_url = reverse_lazy('mainapp:index') # переадресовать что б проверили почту


class RegisterView(View):
    template_name = "authapp/register.html"

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            #user= get_user_model()
            user = authenticate(email=email, password=password)
            print(user)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
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
        return reverse_lazy('authapp:edit', args=[self.request.user.id])

    def get_object(self, queryset=None):  # ограничение на редактирование только своего профиля
        return self.request.user


class EditView(TemplateView):
    pass


class VerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.confirm_email = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('mainapp:index')) # если ок
        return HttpResponseRedirect(reverse('authapp:fail')) # если хуй

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


class FailEmailView(TemplateView):
    template_name = 'authapp/fail_email.html'

class ConfirmEmailView(View):
    template_name = 'authapp/confirm.html'
    def get(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)