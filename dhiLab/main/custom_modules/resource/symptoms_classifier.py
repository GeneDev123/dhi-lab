import json

# Load your JSON file
with open('../json/unique_symptoms.json', 'r') as file:
  dataset = json.load(file)

# Remove spaces in symptom names
for disease, symptoms in dataset.items():
  dataset[disease] = [symptom.strip() for symptom in symptoms]

# Function to rank diseases based on symptoms
def rank_diseases(symptoms):
  ranked_diseases = []

  for disease, disease_symptoms in dataset.items():
    # Calculate the number of matching symptoms
    matches = len(set(symptoms).intersection(disease_symptoms))
    ranked_diseases.append((disease, matches))

  # Sort diseases by the number of matching symptoms (descending)
  ranked_diseases.sort(key=lambda x: x[1], reverse=True)

  return ranked_diseases[:3]  # Return the top 3 ranked diseases

# Input symptoms from the user
user_symptoms = input("Enter symptoms (comma-separated): ").split(',')

# Remove leading/trailing spaces from user input
user_symptoms = [symptom.strip() for symptom in user_symptoms]

# Rank diseases based on user input
top_diseases = rank_diseases(user_symptoms)

# Display the ranked diseases
if top_diseases:
  print("Top 3 likely diseases:")
  for rank, (disease, matches) in enumerate(top_diseases, start=1):
    print(f"{rank}. {disease} ({matches} matching symptom(s))")
else:
  print("No matching diseases found.")