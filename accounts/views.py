from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def manage_users(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        userid = int(request.POST['userid'])
        user = User.objects.get(id=userid)
        user.is_writer = request.POST.get('is_writer') == 'on'
        user.is_solver = request.POST.get('is_solver') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()

        if user == request.user and not user.is_staff:
            return redirect('home')

    user_list = User.objects.all()
    return render(request, 'manage_users.html', {'user_list': user_list})
