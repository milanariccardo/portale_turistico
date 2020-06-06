from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    """Form per la registrazione"""
    email = forms.EmailField(max_length=200, help_text='Required')

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'choose your password wisely'
        self.fields['password2'].widget.attrs['placeholder'] = 'repeat your chosen password'

        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Register', css_class='btn btn-success')
        )
    '''

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2')