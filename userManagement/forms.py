from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Profile

'''
class CustomUserCreationForm(UserCreationForm):
    """Classi per ampliare il model dell'user"""

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = UserCreationForm.Meta.fields + ('avatar',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = UserChangeForm.Meta.fields
'''

class SignupForm(UserCreationForm):
    """Form per la registrazione"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

