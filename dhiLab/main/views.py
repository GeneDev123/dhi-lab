from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm

def register(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    form = CustomUserCreationForm()
  return render(request, 'main/register.html', {'form': form})

def user_login(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('home')
  else:
    form = AuthenticationForm()
  return render(request, 'main/login.html', {'form': form})

def user_logout(request):
  logout(request)
  return redirect('home') 

def home(request):
  return render(request, 'main/home.html')