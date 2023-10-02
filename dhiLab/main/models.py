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

  is_overweight = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_smoking_cigarettes = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_recently_injured = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_high_cholesterol = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_having_hypertension = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)
  is_diabetic = models.CharField(max_length=20, choices=PRESENT_CONDITION_OPTIONS, blank=True, null=True,)  

  def __str__(self):
    return f"{self.first_name} {self.last_name}"