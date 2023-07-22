from django.forms import ModelForm, DateInput, TimeField, TimeInput, TextInput, ModelChoiceField, \
    CheckboxSelectMultiple, NullBooleanField
from crispy_forms.helper import FormHelper
from workplaceapp.models import MainClients
from mainapp.models import Services, News


# форма для добавления нового клиента
# зарегистрированным пользователем
class NewClientForm(ModelForm):
    class Meta:
        model = MainClients
        #fields = '__all__'
        exclude = ['date_created', 'comment']
        widgets = {
            'born_date': DateInput(attrs={'type':'date', 'align':'center'}),
            'born_time': TimeInput(attrs={'type':'time'}),
            'id': TextInput(attrs={'type':'hidden'}),
            'first_name': TextInput(attrs={'readonly':'readonly', 'label':'hhgvudh'}),
            'last_name': TextInput(attrs={'readonly':'readonly', 'type':'hidden'}),
            'user': TextInput(attrs={'type':'hidden'})
        }

    def __init__(self, *args, **kwargs):
        super(NewClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal text-color="red"'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8 text-primary'


