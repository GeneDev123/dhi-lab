from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import CustomUser

# from rest_framework import generics
# from .models import CustomUser
# from .serializers import CustomUserSerializer

from . import chatbot_training
from . import chatbot_utils

def is_admin(user):
  return user.is_superuser or user.is_staff

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
  context = {
    'user_data': request.user,
  }
  return render(request, 'main/profile.html', context)

def update_user_data(request):
  pass


@login_required(login_url='/accounts/login/') 
def home(request):
  print("In Home View")

  # Model and Intents directory
  chatbot_model_dir = "./main/custom_modules/machine-learning-models/chatbot_2023-10-23_04-32-27.h5"
  intents_dir = "./main/custom_modules/json/intents2.json"
  model_data = chatbot_utils.initialize_static_chatbot_requirements(chatbot_model_dir, intents_dir)
  
  if request.method == 'GET':
    user_input = request.GET.get('user_input')
    if user_input:

      intents = chatbot_utils.predict_class(user_input, 
        model_data['model'], 
        model_data['words'], 
        model_data['ignore_chars'],
        model_data['lemmatizer'],  
        model_data['classes'],
      )
      
      chatbot_reply = chatbot_utils.get_response(intents, model_data['data'])
      return JsonResponse({'response': chatbot_reply})
  
  return render(request, 'main/home.html')

@user_passes_test(is_admin, login_url='/accounts/login/')
def chatbot_page(request):
  return render(request, 'main/chatbot-page.html')

@user_passes_test(is_admin, login_url='/custom-page/')
def train_chatbot(request):
  print("In Home View")
  chatbot_training.start_chatbot_training()
  return JsonResponse({'message': 'Function executed successfully'})