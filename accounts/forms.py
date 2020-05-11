from django.contrib.auth.forms import UserCreationForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email',)
        labels = {
            'email': 'Email'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Sign Up')
        )
