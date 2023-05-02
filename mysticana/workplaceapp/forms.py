from django.forms import ModelForm, DateInput, TimeField, TimeInput, TextInput
from crispy_forms.helper import FormHelper
from workplaceapp.models import MainClients

# форма для добавления нового клиента
class AddClientForm(ModelForm):
    class Meta:
        model = MainClients
        #fields = '__all__'
        exclude = ['date_created']
        widgets = {
            'born_date': DateInput(attrs={'type':'date', 'align':'center'}),
            'born_time': TimeInput(attrs={'type':'time'}),
            'id': TextInput(attrs={'type':'hidden'})
        }

    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal text-color="red"'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8 text-primary'