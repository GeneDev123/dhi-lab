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

def filter_symptoms(user_input, symptoms_list):
  filtered_symptoms = [symptom for symptom in symptoms_list if user_input in symptom]
  return filtered_symptoms

def clean_symptom(symptom):
  return symptom.strip().replace(" ", "").replace("_", "").lower()

def classify(symptoms):
  with open("./main/custom_modules/json/unique_symptoms.json") as file:
    dataset = json.load(file)

  user_symptoms = [clean_symptom(symptom) for symptom in symptoms]
  ranked_diseases = []

  for disease, disease_symptoms in dataset.items():
    disease_symptoms = [clean_symptom(symptom) for symptom in disease_symptoms]
    matches = len(set(user_symptoms).intersection(disease_symptoms))
    ranked_diseases.append((disease, matches))

  ranked_diseases.sort(key=lambda x: x[1], reverse=True)

  top_diseases = [(disease, matches) for disease, matches in ranked_diseases if matches > 0]

  classify_output = {
    'top_diseases': top_diseases,
    'dataset_length': len(dataset),
    'dataset': dataset
  }

  return classify_output