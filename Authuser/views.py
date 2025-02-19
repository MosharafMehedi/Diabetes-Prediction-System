from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import regiterForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


def registration(request):
    if request.method == 'POST':
        form=regiterForm (request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')
            form.save()
           
    else:
        form=regiterForm()
    return render(request, 'registration.html', {'form':form})




def user_logout(request):
    logout(request)
    return redirect('login')



class UserLoginView(LoginView):
    template_name = './login.html'
    
    def get_success_url(self):
        return reverse_lazy('predict')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
