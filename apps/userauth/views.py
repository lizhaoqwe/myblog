from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST,require_GET
from .models import User
from utils import restful

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        print(telephone,password,remember)
        user = authenticate(request, telephone=telephone,password=password)
        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(None)
                return restful.ok()
            else:
                request.session.set_expiry(0)
                return restful.ok()
        else:
            return restful.unauth(message='用户名或者密码错误')
    else:
        return restful.params_error(form.get_errors())