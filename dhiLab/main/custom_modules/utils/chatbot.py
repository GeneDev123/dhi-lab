import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Load the preprocessed data
with open("../json/intents.json") as file:
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

# Load the trained model
model = load_model("../machine-learning-models/model_2.h5")

# Define functions for text preprocessing and getting the predicted class
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

# Interactive chat
print("Chatbot: Hi! How can I assist you today? (type 'exit' to end the conversation)")

while True:
  user_input = input("You: ")
  if user_input.lower() == 'exit':
    print("Chatbot: Goodbye! Have a great day!")
    break

  # Get the predicted intent and response from the model
  intents = predict_class(user_input, model)
  bot_response = get_response(intents, data)

  print("Chatbot:", bot_response)
