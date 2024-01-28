from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.html import format_html

admin.site.site_header = "Dr's Lab Administration"

class CustomUserAdmin(UserAdmin):
  model = CustomUser

  # add_form = CustomUserCreationForm # Use the custom creation form for admin dashboard
  # form = CustomUserChangeForm # Use the custom change form for admin dashboard

  list_display = ('display_profile_picture', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_health_care_professional')

  def display_profile_picture(self, obj):
    if obj.profile_picture:
      return format_html('<img src="{}" width="50" height="50" />', obj.profile_picture.url)
    else:
      return 'No Image'
    
  display_profile_picture.short_description = 'Profile Picture'

  fieldsets = (
    (None, 
      {
        'fields': ('username', 'email', 'password')
      }),
      ('Personal info', 
      {
        'fields': 
          ('profile_picture', 'first_name', 'last_name', 'bio', 'age', 'gender')
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
