from django.shortcuts import render, get_object_or_404
from .models import Problem

def home(request):
    problem_list = Problem.objects.all()
    return render(request, 'home.html', {'problem_list': problem_list})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'problem_detail.html', {'problem': problem})

def new_problem(request):
    pass
