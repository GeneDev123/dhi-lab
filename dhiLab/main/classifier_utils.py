import json

def get_disease_list():
  with open("./main/custom_modules/json/unique_symptoms.json") as file:
    data = json.load(file)
  
  disease_names = list(data.keys())
  
  symptoms = []
  for values in data.values():
    symptoms.extend(values)
  
  symptoms = list(set(symptoms))
  symptoms = [symptom.replace('_', ' ') for symptom in symptoms]

  return {
    "disease_names": disease_names,
    "disease_symptoms": symptoms
  }