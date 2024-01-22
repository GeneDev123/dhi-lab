from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
  model = CustomUser

  # add_form = CustomUserCreationForm # Use the custom creation form for admin dashboard
  # form = CustomUserChangeForm # Use the custom change form for admin dashboard

  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_health_care_professional')

  fieldsets = (
    (None, 
      {
        'fields': ('username', 'email', 'password')
      }),
      ('Personal info', 
      {
        'fields': 
          ('first_name', 'last_name', 'bio', 'age', 'gender')
      }),
      ('User Conditions', 
      {
        'fields': 
          ('is_diabetic', 'is_having_hypertension', 'is_high_cholesterol', 'is_overweight', 'is_recently_injured', 'is_smoking_cigarettes')
      }),
      ('Healthcare Professional Information', 
      {
        'fields': (
          'is_health_care_professional', 'specialization', 'education', 'experience',
          'board_certifications', 'professional_affiliations', 'hospital_affiliations',
          'areas_of_expertise', 'patient_reviews_and_ratings', 'office_location',
          'accepted_insurance_plans', 'publications_and_research', 'awards_and_recognitions',
          'contact_phone', 'contact_address', 'contact_website'
        )
      }),
      ('Permissions', 
      {
        'fields': 
          ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
      }),
      ('Important dates', 
      {
        'fields': 
          ('last_login', 'date_joined')
      }),
      ('Agreement', 
      {
        'fields': 
          ('is_agree_terms_and_condition',)
      }),
  )

admin.site.register(CustomUser, CustomUserAdmin)
