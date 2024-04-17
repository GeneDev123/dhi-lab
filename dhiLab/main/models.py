from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

  GENDER = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Not Mention", "not_mention"),
  ]

  PRESENT_CONDITION_OPTIONS = [
    ("TRUE", "true"),
    ("FALSE", "false"),
    ("UNKNOWN", "unknown"),
  ]

  bio = models.TextField(max_length=500, blank=True, null=True)
  first_name = models.CharField(max_length=255, blank=True, null=True,)
  last_name = models.CharField(max_length=255, blank=True, null=True,)
  age = models.IntegerField(blank=True, null=True)
  gender = models.CharField(max_length=20, choices=GENDER, default="Not Mention")
  is_agree_terms_and_condition = models.BooleanField(default=False)
  profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

  is_overweight = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_smoking_cigarettes = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_recently_injured = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_high_cholesterol = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_having_hypertension = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_diabetic = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)  

  is_health_care_professional = models.BooleanField(default=False, null=True, blank=True)
  clinic = models.CharField(max_length=100, null=True, blank=True)
  clinic_loc = models.CharField(max_length=300, null=True, blank=True)
  specialization = models.CharField(max_length=100, null=True, blank=True)
  education = models.TextField(null=True, blank=True)
  experience = models.PositiveIntegerField(null=True, blank=True)
  board_certifications = models.CharField(max_length=200, null=True, blank=True)
  professional_affiliations = models.TextField(null=True, blank=True)
  hospital_affiliations = models.TextField(null=True, blank=True)
  areas_of_expertise = models.TextField(null=True, blank=True)
  patient_reviews_and_ratings = models.TextField(null=True, blank=True)
  office_location = models.TextField(null=True, blank=True)
  accepted_insurance_plans = models.TextField(null=True, blank=True)
  publications_and_research = models.TextField(null=True, blank=True)
  awards_and_recognitions = models.TextField(null=True, blank=True)
  contact_phone = models.CharField(max_length=20, null=True, blank=True)
  contact_address = models.TextField(null=True, blank=True)
  contact_website = models.URLField(null=True, blank=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"