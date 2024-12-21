from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View

from . import forms


class HomePageView(View):
    template = 'authentication/home.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
            
        message = 'Identifiants invalides'
        return render(request, self.template, context={'form':form, 'message':message})


class SignUpView(View):
    template = 'authentication/signup.html'
    form_class = forms.SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if len(form['username'].value()) > 3:
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('flux')
        else:
            message = "Le nom d'utilisateur doit avoir au minimum 4 caractères."
        return render(request, self.template, context={'form': form, 'message': message})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')
    