from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper


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
