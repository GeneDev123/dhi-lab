from django.contrib.auth.forms import UserCreationForm #UserChangeForm,
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = CustomUser
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

  def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Add a class to the email field
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

  def clean_email(self):

    email = self.cleaned_data['email'].lower()
    try:
      account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
    except Exception as e:
      return email
    raise forms.ValidationError('Email "%s" is already in use.' % account)

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
    except  Exception as e:
      return username
    raise forms.ValidationError('Username "%s" is already in use.' % username)

class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'age', 'gender', 'bio',
      'is_overweight', 'is_smoking_cigarettes', 'is_recently_injured',
      'is_high_cholesterol', 'is_having_hypertension', 'is_diabetic', 'is_agree_terms_and_condition']

    def clean_username(self):
      username = self.cleaned_data['username']
      try:
        account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
      except  Exception as e:
        return username
      raise forms.ValidationError('Username "%s" is already in use.' % username)