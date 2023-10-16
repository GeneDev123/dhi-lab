from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from django.http import JsonResponse
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
  print("In Home View")

  # Note: Refactor; This is bad practice 
  # ====================
  model = load_model('./main/custom_modules/machine-learning-models/model_2.h5')
  with open("./main/custom_modules/json/intents.json") as file:
    data = json.load(file)

  words = []
  classes = []
  documents = []
  ignore_chars = ["?", "!", ".", ","]
  lemmatizer = WordNetLemmatizer()

  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      words_list = nltk.word_tokenize(pattern)
      words.extend(words_list)
      documents.append((words_list, intent["tag"]))
      if intent["tag"] not in classes:
        classes.append(intent["tag"])

  words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
  words = sorted(list(set(words)))
  classes = sorted(list(set(classes)))
    
  def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
      return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

  def get_response(intents_list, intents_json):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
      if i["tag"] == tag:
        result = random.choice(i["responses"])
        break
    return result

  def clean_up_sentence(sentence):
    words_list = nltk.word_tokenize(sentence)
    words_list = [lemmatizer.lemmatize(word.lower()) for word in words_list if word not in ignore_chars]
    return words_list

  def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
      for i, word in enumerate(words):
        if word == s:
          bag[i] = 1
          if show_details:
            print(f"Found in bag: {word}")
    return np.array(bag)

  # ====================

  
  if request.method == 'GET':
    user_input = request.GET.get('user_input')
    if user_input:
      # Get the predicted intent and response from the model
      intents = predict_class(user_input, model)
      bot_response = get_response(intents, data)

      print("RESPONSE:")
      print(bot_response)
      return JsonResponse({'response': bot_response})
  
  return render(request, 'main/home.html')