from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
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


class SignupEmail(ModelForm):

    class Meta:
        model = Profile
        fields = ('email',)


class SignupForm(UserCreationForm):
    """Form per la registrazione"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'choose your password wisely'
        self.fields['password2'].widget.attrs['placeholder'] = 'repeat your chosen password'
        '''
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Register', css_class='btn btn-success')
        )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
