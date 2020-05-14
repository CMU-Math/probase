from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, UserPermissionsForm
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
        user = User.objects.get(id=request.POST['userid'])
        data = {
            'is_writer': request.POST.get('is_writer') == 'on',
            'is_solver': request.POST.get('is_solver') == 'on',
            'is_staff': request.POST.get('is_staff') == 'on',
        }
        form = UserPermissionsForm(data, instance=user)
        assert(form.is_valid())
        form.save()

    # if staff makes themselves non-staff, they shouldn't be allowed to make more changes
    # this doesn't seem to be working though
    if not request.user.is_staff:
        raise PermissionDenied

    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})
