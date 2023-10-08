from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# from rest_framework import generics
# from .models import CustomUser
# from .serializers import CustomUserSerializer

def user_login_and_register(request, login_or_register_param):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    print(login_or_register_param)
    if login_or_register_param == 'login':
      form = AuthenticationForm(request, request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    elif login_or_register_param == 'register':  
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
  else:
    form = CustomUserCreationForm if login_or_register_param == 'register' else AuthenticationForm()

  return render(request, 'main/login-and-register.html', {'form': form, 'login_or_register': login_or_register_param})

def user_logout(request):
  logout(request)
  return redirect('home') 

# class CustomUserList(generics.ListCreateAPIView):
#   queryset = CustomUser.objects.all()
#   serializer_class = CustomUserSerializer

# class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
#   queryset = CustomUser.objects.all()
#   serializer_class = CustomUserSerializer

@login_required(login_url='/accounts/login/')
def user_profile(request):
  print("In profile view")
  return render(request, 'main/profile.html')

@login_required(login_url='/accounts/login/') 
def home(request):
  print("In home page")
  return render(request, 'main/home.html')