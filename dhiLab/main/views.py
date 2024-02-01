from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser

from . import chatbot_training
from . import chatbot_utils
from . import classifier_utils

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

@login_required(login_url='/accounts/login/')
def user_profile(request, is_updating_user_data):
  print("In profile view")
  
  context = {
    'user_data': request.user,
    'is_updating_data': 1 if is_updating_user_data == 1 else 0,
  }

  if request.method == 'POST' and is_updating_user_data == 1:
    form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your profile has been updated successfully.')
      return redirect('user-profile', is_updating_user_data=0)
    else:
      messages.error(request, 'There was an error in updating your profile. Please correct the errors.')
  else:
    form = UserUpdateForm(instance=request.user)

  context['form'] = form
  return render(request, 'main/profile.html', context)

def update_user_data(request):
  pass


@login_required(login_url='/accounts/login/') 
def home(request):
  print("In Home View")

  context = {}

  request.session['hide_welcome'] = True

  disease = classifier_utils.get_disease_list()
  disease_list = disease["disease_names"]
  symptoms = disease["disease_symptoms"]
  
  context['disease_list'] = sorted(disease_list)
  context['symptoms'] = sorted(symptoms)

  # Model and Intents directory
  chatbot_model_dir = "./main/custom_modules/machine-learning-models/chatbot_2024-01-20_22-36-19.h5"
  intents_dir = "./main/custom_modules/json/intents3.json"
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
  
  return render(request, 'main/home.html', context)

def filter_symptoms(request):
  query = request.GET.get("query", "")
  disease = classifier_utils.get_disease_list()
  filtered_symptoms = classifier_utils.filter_symptoms(query, disease["disease_symptoms"])
  return JsonResponse(filtered_symptoms, safe=False)

def classify_symptoms(request):
  selected_symptoms = request.GET.getlist('selected_symptoms[]')
  classification = classifier_utils.classify(selected_symptoms)

  return JsonResponse({
    'diseases': classification['top_diseases'][:3], 
    'totalDataset': classification['dataset_length'],
    'dataset': classification['dataset'],
  }, safe=False)

@user_passes_test(is_admin, login_url='/accounts/login/')
def chatbot_page(request):
  return render(request, 'main/chatbot-page.html')

@user_passes_test(is_admin, login_url='/custom-page/')
def train_chatbot(request):
  print("In Home View")

  data  = chatbot_training.start_chatbot_training()
  return JsonResponse({
    'message': 'Function executed successfully',
    'data': data
  })
  
@login_required(login_url='/accounts/login/') 
def doctors_page(request):
  context = {}

  healthcare_professionals = CustomUser.objects.filter(is_health_care_professional=True)
  
  context['health_care_prof'] = healthcare_professionals
  return render(request, 'main/doctors-page.html', context)

