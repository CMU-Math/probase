from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import PermissionDenied
from .models import Problem
from .forms import NewProblemForm, EditProblemForm

def home(request):
    problem_list = Problem.objects.all().order_by('-creation_time')
    return render(request, 'home.html', {'problem_list': problem_list})

@login_required
def problem_detail(request, problem_id):
    if not request.user.is_writer and not request.user.is_staff:
        raise PermissionDenied
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'problem_detail.html', {'problem': problem})

@login_required
def new_problem(request):
    if not request.user.is_writer and not request.user.is_staf:
        raise PermissionDenied
    if request.method == 'POST':
        data = {
            'preview': True,
            'title': request.POST['title'],
            'problem_text': request.POST['problem_text'],
            'answer': request.POST['answer'],
            'solution': request.POST['solution'],
        }
        if request.POST.get('cancel'):
            return redirect('home')
        elif request.POST.get('preview'):
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
                # if currently showing preview, continue to show preview
                # also show error messages
                if request.POST['showing-preview'] == 'True':
                    data['form'] = form
                    return render(request, 'new_problem.html', data)
                else:
                    return render(request, 'new_problem.html', {'form': form})
    else:
        form = NewProblemForm()
        return render(request, 'new_problem.html', {'form': form })

@login_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.user != problem.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        data = {
            'preview': True,
            'title': request.POST['title'],
            'problem_text': request.POST['problem_text'],
            'answer': request.POST['answer'],
            'solution': request.POST['solution'],
        }
        if request.POST.get('delete'):
            problem.delete()
            return redirect('home')
        if request.POST.get('cancel'):
            return redirect('problem_detail', problem_id=problem_id)
        elif request.POST.get('preview'):
            form = EditProblemForm(initial=data)
            data['form'] = form
            return render(request, 'edit_problem.html', data)
        else:
            assert(request.POST.get('save'))
            form = EditProblemForm(request.POST, instance=problem)
            if form.is_valid():
                form.save()
                return redirect('problem_detail', problem_id=problem_id)
            else:
                # if currently showing preview, continue to show preview
                # also show error messages
                if request.POST['showing-preview'] == 'True':
                    data['form'] = form
                    return render(request, 'edit_problem.html', data)
                else:
                    return render(request, 'edit_problem.html', {'form': form})
    else:
        form = EditProblemForm(instance=problem)
        return render(request, 'edit_problem.html', {'form': form })
