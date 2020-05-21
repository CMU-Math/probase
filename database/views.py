from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import PermissionDenied
from .forms import ProblemForm, RatingForm, ProblemSelect, ProblemSelector
from .models import Problem, Rating


import json
from django.core.serializers.json import DjangoJSONEncoder
from django_tex.shortcuts import render_to_pdf

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
    # filter/my problems and stuff should be implemented here
    if not request.user.is_solver and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        problem_list = [Problem(**temp) for temp in json.loads(request.POST['problem_list'])]
        template_name = 'test.tex'
        context = {'solutions': True, 'problem_list' : problem_list}
        return render_to_pdf([], template_name, context, filename='test.pdf')
    else: 
        problem_list = Problem.objects.all().order_by('-creation_time')
        empty_message = 'There are no problems in the database yet.'

        context = {
            'filter': 0,
            'form': ProblemSelect(),
            'data': json.dumps(list(Problem.objects.values().order_by('-creation_time')), cls = DjangoJSONEncoder),
            'empty_message': empty_message,
        }
        return render(request, 'problem_list.html', context)

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if not request.user.is_solver and not request.user.is_staff and request.user != problem.author:
        raise PermissionDenied
    if request.method == 'POST':
        assert request.POST.get('submit')
        if request.POST['submit'] == 'delete':
            problem.delete()
            return redirect('home')
        elif request.POST['submit'] == 'rate':
            old_rating = problem.ratings.filter(user=request.user).first()
            if old_rating:
                old_rating.delete()
            diff = int(request.POST['diff'])
            qual = int(request.POST['qual'])
            new_rating = Rating(problem=problem, user=request.user, difficulty=diff, quality=qual)
            new_rating.save()
        else:
            assert False, "invalid submit"

    current_rating = problem.ratings.filter(user=request.user).first()
    diff_freq, diff_percent = problem.diff_distribution()
    qual_freq, qual_percent = problem.qual_distribution()

    return render(request, 'problem_detail.html', {
        'problem': problem,
        'current_rating': current_rating,
        'diff_text': Rating.DIFF.values(),
        'diff_freq': diff_freq,
        'diff_percent_color': [(diff_percent[i], Rating.COLORS[i]) for i in range(5)],
        'qual_text': Rating.QUAL.values(),
        'qual_freq': qual_freq,
        'qual_percent_color': [(qual_percent[i], Rating.COLORS[i]) for i in range(5)],
    })

@login_required
def new_problem(request):
    if not request.user.is_writer and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        data = {
            'preview': True,
            'subject': request.POST['subject'],
            'title': request.POST['title'],
            'problem_text': request.POST['problem_text'],
            'answer': request.POST['answer'],
            'solution': request.POST['solution'],
        }
        if request.POST.get('preview'):
            form = ProblemForm(initial=data)
            data['form'] = form
            return render(request, 'make_problem.html', data)
        else:
            assert request.POST.get('submit')
            form = ProblemForm(request.POST)
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
                    return render(request, 'make_problem.html', data)
                else:
                    return render(request, 'make_problem.html', {'form': form})
    else:
        form = ProblemForm()
        return render(request, 'make_problem.html', {'form': form })

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
            form = ProblemForm(initial=data)
            data['form'] = form
            return render(request, 'make_problem.html', data)
        else:
            assert request.POST.get('submit')
            form = ProblemForm(request.POST, instance=problem)
            if form.is_valid():
                form.save()
                return redirect('problem_detail', problem_id=problem_id)
            else:
                # if currently showing preview, continue to show preview
                # also show error messages
                if request.POST['showing-preview'] == 'True':
                    data['form'] = form
                    return render(request, 'make_problem.html', data)
                else:
                    return render(request, 'make_problem.html', {'form': form})
    else:
        form = ProblemForm(instance=problem)
        return render(request, 'make_problem.html', {'form': form })

