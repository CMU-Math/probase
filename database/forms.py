from django.forms import ModelForm, Textarea
from .models import Problem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Button, ButtonHolder, HTML, Field
from crispy_forms.bootstrap import FormActions

class NewProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ('title', 'problem_text', 'answer', 'solution')
        labels = {
            'problem_text': 'Problem'
        }
        widgets = {
            'problem_text': Textarea(attrs={'rows': 6}),
            'solution': Textarea(attrs={'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', autocomplete="off"),
            Field('problem_text', autocomplete="off"),
            Field('answer', autocomplete="off"),
            Field('solution', autocomplete="off"),
            ButtonHolder(
                HTML('<a href={% url "home" %} class="btn btn-secondary">Cancel</a> '),
                Submit('submit', 'Submit', formnovalidate=''),
                Submit('preview', 'Preview', formnovalidate=''),
                css_class='mb-5',
            ),
        )

