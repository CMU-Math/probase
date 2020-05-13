from django.forms import ModelForm, Textarea
from .models import Problem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Button, ButtonHolder, HTML, Field
from crispy_forms.bootstrap import FormActions

# These forms are very similar, maybe we should combine them?

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
            FormActions(
                Submit('submit', 'Submit', css_class='mx-1', formnovalidate=''),
                Submit('cancel', 'Cancel', css_class='btn-secondary float-left mx-1', formnovalidate=''),
                Submit('preview', 'Preview', css_class='btn-info float-left mx-1', formnovalidate=''),
                css_class='mb-5 text-left',
            ),
        )

class EditProblemForm(ModelForm):
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
            FormActions(
                Submit('save', 'Save', css_class='mx-1', formnovalidate=''),
                Submit('delete', 'Delete', css_class='btn-danger float-left mx-1', formnovalidate=''),
                Submit('cancel', 'Cancel', css_class='btn-secondary float-left mx-1', formnovalidate=''),
                Submit('preview', 'Preview', css_class='btn-info float-left mx-1', formnovalidate=''),
                css_class='mb-5 text-left',
            ),
        )


