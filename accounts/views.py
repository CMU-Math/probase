from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm

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
        return PermissionDenied
    return 
