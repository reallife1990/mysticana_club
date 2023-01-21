from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from authapp.utils import send_email_for_verify
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib import messages


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal text-color="red"'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8 text-primary'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class AuthenticationForm(DjangoAuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        print(username)
        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            print(self.user_cache)
            if self.user_cache is None:
                messages.add_message(self.request, messages.WARNING,
                                     f"Имя пользователя и(или) пароль не верны, проверьте данные и повторите")
                raise self.get_invalid_login_error()
            elif not self.user_cache.confirm_email:
                send_email_for_verify(self.request, self.user_cache)

                messages.add_message(self.request, messages.WARNING,
                                     f"Ваш email не подтверждён. На {self.user_cache.email}"
                                     f"отправлены инструкции для завершения регистрации")
                raise ValidationError(
                    'Email not verify, check your email',
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
