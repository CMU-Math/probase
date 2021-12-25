from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import PermissionDenied
from .forms import ProblemForm, RatingForm, ProblemSelect, ProblemSelector, ProblemFilter
from .models import Problem, Rating, Comment
from django_tex.shortcuts import render_to_pdf
from taggit.models import Tag


def home(request):
    if request.user.is_authenticated:
        if request.user.is_solver or request.user.is_staff:
            return redirect('all_problems')
        elif request.user.is_writer:
            return redirect('my_problems')
        else:
            staff_list = get_user_model().objects.filter(is_active=True, is_staff=True).order_by('pk')
            return render(request, 'home.html', {'staff_list': staff_list})
    return render(request, 'home.html')


# @login_required
# def all_problems(request):
#     if not request.user.is_solver and not request.user.is_staff:
#         raise PermissionDenied
#     problem_list = Problem.objects.filter(is_archived=False).order_by('-creation_time')
#     empty_message = 'There are no problems in the database yet.'
#     return render(request, 'problem_list.html', {
#         'problem_list': problem_list,
#         'empty_message': empty_message,
#     })

def filtercat(tag_list, problem_list, request):
    request_list = request.GET.getlist('tag_filter')
    if "" in request_list:
        return problem_list
    # result_list = Model.objects.none()
    # for request_tag in request_list:
    #     result_list = result_list | problem_list.filter()
    return problem_list.filter(tags__name__in=request_list).distinct()


@login_required
def all_problems(request):
    if not request.user.is_solver and not request.user.is_staff:
        raise PermissionDenied
    problem_list = Problem.objects.filter(is_archived=False).order_by('-creation_time')
    empty_message = 'There are no problems in the database yet.'
    total_tag_list = Tag.objects.all()
    # print(tag_list.first())
    # tag_list = Problem.objects.values_list('tags', flat=True).distinct()
    problem_list = filtercat(total_tag_list, problem_list, request)
    return render(request, 'problem_list.html', {
        'problem_list': problem_list,
        'empty_message': empty_message,
        'tags': total_tag_list,
        'form':ProblemFilter
    })

@login_required
def my_problems(request):
    if not request.user.is_writer and not request.user.is_staff:
        raise PermissionDenied
    problem_list = Problem.objects.filter(author=request.user, is_archived=False).order_by('-creation_time')
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
    if request.method == 'POST':
        print(request.POST)
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
        elif request.POST['submit'] == 'newComment':
            comment = Comment(problem=problem, author=request.user, text=request.POST['text'])
            comment.save()
        elif request.POST['submit'] == 'editComment':
            comment = Comment.objects.get(pk=request.POST['commentID'])
            comment.text = request.POST['text']
            comment.save()
        elif request.POST['submit'] == 'addTag':
            problem.tags.add(request.POST['tag'])
            problem.save()
            return JsonResponse({})
        elif request.POST['submit'] == 'removeTag':
            text = request.POST['tag']
            problem.tags.remove(text)
            problem.save()
            if Problem.objects.filter(tags__name__in=[text]).count() == 0:
                tag = Tag.objects.filter(name=text)
                tag.delete()
            return JsonResponse({})
        else:
            assert False, "invalid submit"

    current_rating = problem.ratings.filter(user=request.user).first()
    diff_freq, diff_percent = problem.diff_distribution()
    qual_freq, qual_percent = problem.qual_distribution()
    comment_list = problem.comments.order_by('creation_time')
    print(problem.tags.all())

    return render(request, 'problem_detail.html', {
        'problem': problem,
        'current_rating': current_rating,
        'diff_text': Rating.DIFF.values(),
        'diff_freq': diff_freq,
        'diff_percent_color': [(diff_percent[i], Rating.COLORS[i]) for i in range(5)],
        'qual_text': Rating.QUAL.values(),
        'qual_freq': qual_freq,
        'qual_percent_color': [(qual_percent[i], Rating.COLORS[i]) for i in range(5)],
        'comment_list': comment_list,
        'tag_list': problem.tags.all(),
        'all_tags': Tag.objects.order_by('name'),
    })

@login_required
def new_problem(request):
    if not request.user.is_writer and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        print(request.POST)
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
                problem.tags.add(problem.get_subject_display().lower())
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
        return render(request, 'make_problem.html', {'form': form})

@login_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.user != problem.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        print(request.POST)
        data = {
            'preview': True,
            'subject': request.POST['subject'],
            'title': request.POST['title'],
            'problem_text': request.POST['problem_text'],
            'answer': request.POST['answer'],
            'solution': request.POST['solution'],
        }
        if request.POST.get('delete'):
            problem.delete()
            return redirect('home')
        elif request.POST.get('preview'):
            form = ProblemForm(initial=data)
            data['form'] = form
            return render(request, 'make_problem.html', data)
        else:
            assert request.POST.get('submit')
            form = ProblemForm(request.POST, instance=problem)
            if form.is_valid():
                form.save()
                problem.tags.add(problem.get_subject_display().lower())
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
        return render(request, 'make_problem.html', {'form': form})

@login_required
def create_test(request):
    # filter/my problems and stuff should be implemented here
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        if "to_pdf" in request.POST:
            #submission = ProblemSelect(request.POST)
            template_name = 'test.tex'
            problem_list = Problem.objects.filter(id__in=request.POST.getlist('problems')).order_by('-creation_time')
            context = {'solutions': True, 'problem_list' : problem_list}
            return render_to_pdf(request, template_name, context, filename='test.pdf')
        elif "filter" in request.POST:
            print("")
    else: 
        problem_list = Problem.objects.all().order_by('-creation_time')
        empty_message = 'There are no problems in the database yet.'

        return render(request, 'create_test.html', {
            'filter': 0,
            'form': ProblemSelect(problems=problem_list),
            'empty_message': empty_message,
        })
