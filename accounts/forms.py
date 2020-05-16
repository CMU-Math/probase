from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field, Hidden, Button
from crispy_forms.bootstrap import FormActions

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
        self.helper.label_class = 'col-sm-3 col-md-2'
        self.helper.field_class = 'col-sm-9 col-md-10'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            FormActions(
                Submit('submit', 'Sign Up'),
                css_class='form-group row',
            )
        )
