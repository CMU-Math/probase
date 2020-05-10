from django.contrib.auth.forms import UserCreationForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'password1',
            'password2',
            Submit('submit', 'Sign Up')
        )
