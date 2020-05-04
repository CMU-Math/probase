from django.forms import ModelForm
from .models import Problem

class NewProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'problem_text', 'answer', 'solution']
