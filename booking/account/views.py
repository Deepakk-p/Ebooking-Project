from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,CreateView,ListView
from django.views import View
# from user.models import Hotel
from .models import *
from .forms import LoginForm,RegForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

class LandingView(TemplateView):
    template_name='landing.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name='login.html'
    def post(self, request, *args, **kwargs):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(username=uname,password=pswd)
            user_obj=User.objects.filter(username=uname)
            # if user_obj.exists:
            #     messages.warning(request, "User  already exists")
            #     return redirect('login')
            if user:
                login(request,user)
                messages.success(request,"Login successful !!")
                return redirect('main')
            else:
                messages.error(request,"Login failed!!!")
                return redirect('login')
        else:
            return render(request, 'login.html',{"form":form_data})


class RegView(CreateView):
    form_class = RegForm
    template_name='reg.html'   
    success_url=reverse_lazy('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        if logout:
            messages.success(request,"Logout successful")
            return redirect('login')
    

class MainView(TemplateView):
    template_name='main.html'