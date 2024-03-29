from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Problem, Rating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from django.template.loader import get_template
from django.utils.text import normalize_newlines

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

    def clean_problem_text(self):
        data = self.cleaned_data['problem_text']
        data = normalize_newlines(data)
        return data

    def clean_solution(self):
        data = self.cleaned_data['solution']
        data = normalize_newlines(data)
        return data

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

class ProblemSelector(ModelMultipleChoiceField):
    def label_from_instance(self, prob):
        return get_template('includes/problem_card.html').render({'problem': prob})

class ProblemSelect(forms.Form):
    problems = ProblemSelector(widget=CheckboxSelectMultiple(), queryset=None)
    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'problems' in kwargs:
            self.fields['problems'].queryset = kwargs['problems']
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FormActions(
                Field('problems'),
                Submit('to_pdf', 'To PDF', css_class='mx-1'),
            ),
        )

# class ProblemFilter(ModelForm):
#     class Meta:
#         model = Problem
#         fields = []
