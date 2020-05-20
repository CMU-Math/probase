from django.forms import ModelForm, Textarea, TextInput, NumberInput
from .models import Problem, Rating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ('subject', 'title', 'problem_text', 'answer', 'solution')
        labels = {
            'problem_text': 'Problem'
        }
        widgets = {
            'problem_text': Textarea(attrs={
                'rows': 6,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px"',
            }),
            'solution': Textarea(attrs={
                'rows': 6,
                'oninput': 'this.style.height = "";this.style.height = this.scrollHeight + "px"',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('subject', css_class="custom-select"),
            Field('title', autocomplete="off"),
            Field('problem_text', autocomplete="off"),
            Field('answer', autocomplete="off"),
            Field('solution', autocomplete="off"),
            FormActions(
                Submit('submit', '{% url \'new_problem\' as url_new %}{% if request.get_full_path == url_new %}Add Problem{% else %}Save Changes{% endif %}', css_class='mx-1', formnovalidate=''),
                Submit('preview', 'Preview', css_class='btn-info mx-1', formnovalidate=''),
                css_class='mb-5',
            ),
        )

class RatingForm(ModelForm):

    class Meta:
        model = Rating
        fields = ('difficulty', 'quality')
        widgets = {
            'difficulty': NumberInput(attrs={
                'min': 1,
                'max': 10,
            }),
            'quality': NumberInput(attrs={
                'min': 1,
                'max': 10,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('difficulty'),
            Field('quality'),
        )

