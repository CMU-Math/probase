from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django import forms
from .models import Problem
from .forms import NewProblemForm

def home(request):
    problem_list = Problem.objects.all()
    return render(request, 'home.html', {'problem_list': problem_list})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'problem_detail.html', {'problem': problem})

def new_problem(request):
    if request.method == 'POST':
        form = NewProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.author = User.objects.first() # temporary
            problem.save()
            return redirect('problem_detail', problem_id=problem.id)
    else:
        form = NewProblemForm()
    return render(request, 'new_problem.html', {'form': form})
