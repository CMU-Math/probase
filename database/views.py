from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import PermissionDenied
from .models import Problem
from .forms import NewProblemForm, EditProblemForm

def home(request):
    if request.user.is_authenticated:
        if request.user.is_solver or request.user.is_staff:
            return redirect('all_problems')
        elif request.user.is_writer:
            return redirect('my_problems')
        else:
            staff_list = get_user_model().objects.filter(is_staff=True)
            return render(request, 'home.html', {'staff_list': staff_list})
    return render(request, 'home.html')

@login_required
def all_problems(request):
    if not request.user.is_solver and not request.user.is_staff:
        raise PermissionDenied
    problem_list = Problem.objects.all().order_by('-creation_time')
    empty_message = 'There are no problems in the database yet.'
    return render(request, 'problem_list.html', {
        'problem_list': problem_list,
        'empty_message': empty_message,
    })

@login_required
def my_problems(request):
    if not request.user.is_writer and not request.user.is_staff:
        raise PermissionDenied
    problem_list = Problem.objects.filter(author=request.user).order_by('-creation_time')
    empty_message = "You haven't submitted any problems yet."
    return render(request, 'problem_list.html', {
        'problem_list': problem_list,
        'empty_message': empty_message,
    })

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if not request.user.is_solver and not request.user.is_staff and request.user != problem.author:
        raise PermissionDenied
    return render(request, 'problem_detail.html', {'problem': problem})

@login_required
def new_problem(request):
    if not request.user.is_writer and not request.user.is_staff:
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
            assert(request.POST.get('add_problem'))
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
            print('preview')
            print(data['problem_text'])
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
