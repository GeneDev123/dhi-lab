import random
import json
import pickle
import numpy as np
import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.callbacks import CSVLogger

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from pathlib import Path
import os 

def training_chatbot_new():
  # Download NLTK data (if not already downloaded)
  nltk.download("punkt")
  nltk.download("wordnet")

  # Load and preprocess intents.json data
  with open("../json/intents2.json") as file:
    data = json.load(file)

  words = []
  classes = []
  documents = []
  ignore_chars = ["?", "!", ".", ","]
  lemmatizer = WordNetLemmatizer()

  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      # Tokenize and lemmatize words
      words_list = nltk.word_tokenize(pattern)
      words.extend(words_list)
      documents.append((words_list, intent["tag"]))
      if intent["tag"] not in classes:
        classes.append(intent["tag"])

  # Lemmatize and remove duplicates
  words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
  words = sorted(list(set(words)))

  # Sort classes
  classes = sorted(list(set(classes)))

  # Create training data
  training_data = []
  output_empty = [0] * len(classes)
  for document in documents:
    bag = []
    pattern_words = document[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
      bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training_data.append((bag, output_row))

  random.shuffle(training_data)
  X_train = np.array([data[0] for data in training_data])
  y_train = np.array([data[1] for data in training_data])
  # training_data = np.array(training_data)

  # # Split data into X and y
  # X_train = list(training_data[:, 0])
  # y_train = list(training_data[:, 1])

  # Build the Neural Network
  model = Sequential()
  model.add(Dense(128, input_shape=(len(X_train[0]),), activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(64, activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(len(y_train[0]), activation="softmax"))

  # Compile the model
  sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
  model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

  # Train the model
  model.fit(np.array(X_train), np.array(y_train), epochs=2000, batch_size=10, verbose=1)

  # Save the model
  model.save("chatbot_model.h5")
  print("Model trained and saved as chatbot_model.h5")

  # Rest of the code will be in a separate chatbot.py file for the user to run the chatbot interactively`

training_chatbot_new()