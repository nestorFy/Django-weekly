from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import ModelBackend
from django.views.generic import View
from .forms import LoginForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import RegisterForm, UserForm
from .models import UserProfile
from django.db.models import Q


class CustomBackend(ModelBackend):
    """重写用户登陆
    使用用户名和密码都能登陆
    """

    def authenticate(username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        request.session['login_form'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = CustomBackend.authenticate(username=username, password=password)
        except Exception as e:
            user = None
        if user is not None:
            login(request, user)
            request.session['is_login'] = True
            request.session['user_id'] = str(user.id)
            request.session['user_name'] = str(user)
            return HttpResponseRedirect(request.session['login_form'])
        else:
            return render(request, 'users/login.html',
                          {'msg': "Your username and password didn't match. Please try again."})


def custom_login(request):
    if request.method == "POST":
        # 获取seesion中的用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = CustomBackend.authenticate(username=username, password=password)
        print(username, password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'weekly/index.html')
            else:
                return render(request, 'users/login.html', {'msg': 'User not exist.'})
        else:
            return render(request, 'users/login.html',
                          {'msg': "Your username and password didn't match. Please try again."})
    elif request.method == "GET":
        return render(request, 'users/login.html')


def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('weekly:index'))


class UsersView(ListView):
    context_object_name = 'users'
    form_class = UserForm
    model = UserProfile
    template_name = 'users/users.html'
    success_url = '/users/'


class UserAddView(CreateView):
    """增加一条将要写的周报记录"""
    form_class = UserForm
    template_name = "users/user_add.html"
    success_url = '/users/user_list/'
