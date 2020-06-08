import os, shutil

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from portaleTuristico.settings import MEDIA_ROOT

from .models import Profile


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


class UpdateUserSettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        image = self.cleaned_data['avatar']
        profilo = Profile.objects.get(pk=self.instance.pk)

        if image is not None:
            folder = os.path.join(MEDIA_ROOT, 'user_' + str(self.instance.pk))
            if os.path.isdir(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
            profilo.avatar = image

        profilo.save()
        user.save()

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
        labels = {
            'first_name': _('Nome'),
            'last_name': _('Cognome'),
        }