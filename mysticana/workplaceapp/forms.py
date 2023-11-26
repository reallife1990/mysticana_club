from uuid import uuid4

from django.forms import ModelForm, DateInput, TimeField, TimeInput, TextInput
from crispy_forms.helper import FormHelper
from workplaceapp.models import MainClients, ServiceClients
from mainapp.models import Services, News


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



class ServiceChangeForm(ModelForm):

    class Meta:
        model = Services
        fields = (
            'title',
            'preamble',
            'body',
            'image',
            'price',
            'length_time',
            'deleted'
        )

class ServiceAddForm(ModelForm):

    class Meta:
        model = Services
        fields = '__all__'

class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = '__all__'



"Добавление консультации"
class AddClientService(ModelForm):

    def __init__(self, *args, **kwargs):
        # фильтрация только активных услуг
        super(AddClientService, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Services.objects.filter(deleted=False)

    class Meta:
        model = ServiceClients
        fields =('client','date','service','price','comment')
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'align': 'center'}),
            'client' : TextInput(attrs={'type':'hidden'})

        }