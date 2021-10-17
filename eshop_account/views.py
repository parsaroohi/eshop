from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm, EditUserForm
from django.contrib.auth import login,get_user_model,authenticate
from django.contrib.auth.models import User

# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name=login_form.cleaned_data.get('user_name')
        password=login_form.cleaned_data.get('password')
        user=authenticate(request,username=user_name,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            login_form.add_error('user_name','کاربری با مشخصات وارد شده یافت نشد.')
    context={
        'loginForm':login_form
    }
    return render(request,'account/login.html',context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    registerForm=RegisterForm(request.POST or None)
    if registerForm.is_valid():
        username=registerForm.cleaned_data.get('username')
        password=registerForm.cleaned_data.get('password')
        email=registerForm.cleaned_data.get('email')
        User.objects.create_user(username=username,password=password,email=email)
        return redirect('/login')
    context={
        'registerForm':registerForm
    }
    return render(request,'account/register.html',context)


def logout(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def user_account_main_page(request):
    context={}
    return render(request,'account/user_account_main.html',context)


@login_required(login_url='/login')
def edit_user_profile(request):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    if user is None:
        raise Http404('کاربر موردنظر یافت نشد.')

    edit_user_form=EditUserForm(request.POST or None,initial={'first_name':user.first_name,'last_name':user.last_name})
    if edit_user_form.is_valid():
        first_name=edit_user_form.cleaned_data.get('first_name')
        last_name=edit_user_form.cleaned_data.get('last_name')
        user.first_name=first_name
        user.last_name=last_name
        user.save()

    context={
        'edit_form':edit_user_form
    }
    return render(request,'account/edit_account.html',context)


def user_sidebar(request):
    context={}
    return render(request,'account/user_sidebar.html',context)