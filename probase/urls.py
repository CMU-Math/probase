from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from database import views
from accounts import views as account_views

urlpatterns = [
    path('', views.home, name='home'),
    path('all/', views.all_problems, name='all_problems'),
    path('mine/', views.my_problems, name='my_problems'),
    path('new/', views.new_problem, name='new_problem'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:problem_id>/edit/', views.edit_problem, name='edit_problem'),

    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
#    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),

    path('admin/', admin.site.urls),
]
