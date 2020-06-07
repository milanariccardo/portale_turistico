from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView

from userManagement.forms import SignupForm
from userManagement.models import Profile

accountActivationToken = PasswordResetTokenGenerator()


# class Registration(CreateView):
#     form_class = SignupForm
#     template_name = 'registration/registration.html'
#     success_url = reverse_lazy('login')

def Registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = SignupForm()

    context = {'form': form,}
    return render(request, 'registration/registration.html', context)