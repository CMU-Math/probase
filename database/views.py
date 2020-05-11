from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Problem
from .forms import NewProblemForm

def home(request):
    problem_list = Problem.objects.all().order_by('-creation_time')
    return render(request, 'home.html', {'problem_list': problem_list})

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'problem_detail.html', {'problem': problem})

@login_required
def new_problem(request):
    if request.method == 'POST':
        if request.POST.get('preview'):
            data = {
                'preview': 'true', # nonempty string used as variable to show preview
                'title': request.POST['title'],
                'problem_text': request.POST['problem_text'],
                'answer': request.POST['answer'],
                'solution': request.POST['solution'],
            }
            form = NewProblemForm(initial=data)
            data['form'] = form
            return render(request, 'new_problem.html', data)
        else:
            assert(request.POST.get('submit'))
            form = NewProblemForm(request.POST)
            if form.is_valid():
                problem = form.save(commit=False)
                problem.author = request.user
                problem.save()
                return redirect('problem_detail', problem_id=problem.id)
    else:
        form = NewProblemForm()
    return render(request, 'new_problem.html', {'form': form })
