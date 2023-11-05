import random
import json
import datetime
import numpy as np

import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

def training_chatbot_new():
  nltk.download("punkt")
  nltk.download("wordnet")

  with open("./main/custom_modules/json/intents2.json") as file:
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

  # Neural Network
  model = Sequential()
  model.add(Dense(120, input_shape=(len(X_train[0]),), activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(64, activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(len(y_train[0]), activation="softmax"))

  # Compile the model
  sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
  model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

  # Train the model
  model.fit(np.array(X_train), np.array(y_train), epochs=300, batch_size=10, verbose=1)

  # Save the model
  current_datetime = datetime.datetime.now()
  formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
  model_name = f"./main/custom_modules/machine-learning-models/chatbot_{formatted_datetime}.h5"
  model.save(model_name)

  X_test = np.array([data[0] for data in training_data])
  y_test = np.array([data[1] for data in training_data])
  y_pred = model.predict(X_test)
  y_pred_classes = np.argmax(y_pred, axis=1)
  y_true = np.argmax(y_test, axis=1)

  accuracy = accuracy_score(y_true, y_pred_classes)
  precision = precision_score(y_true, y_pred_classes, average='weighted')
  recall = recall_score(y_true, y_pred_classes, average='weighted')
  f1 = f1_score(y_true, y_pred_classes, average='weighted')

  target_names = [classes[i] for i in range(len(classes))]
  report = classification_report(y_true, y_pred_classes, target_names=target_names)
  
  print(report)

  returnOutput = {
    "accuracy:": str(round(accuracy, 4) * 100) + "%",
    "precision:": str(round(precision, 4) * 100) + "%",
    "recall:": str(round(recall, 4) * 100) + "%",
    "f1Score:": str(round(f1, 4) * 100) + "%",
    "report": report,
  }

  return returnOutput

def start_chatbot_training(): 
  return training_chatbot_new()