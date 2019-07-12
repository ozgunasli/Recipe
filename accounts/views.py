
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request,'accounts/login.html',{'form':form})
        login(request,user)
        return redirect('index')

    return render(request, 'accounts/login.html', {'form': form})



def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.is_superuser = True
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        return redirect('index')


    return render(request, "accounts/register.html", {"form": form, 'title': 'Üye Ol'})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')