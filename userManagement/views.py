from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView

from userManagement.forms import SignupForm, UpdateUserSettingsForm

accountActivationToken = PasswordResetTokenGenerator()


class Registration(CreateView):
    form_class = SignupForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('confirmRegistration')

    def form_valid(self, form):
        response = super(Registration, self).form_valid(form)
        mailSubject = "Mail per la conferma d'iscrizione"
        confirmUrl = reverse('verifyUserEmail', args=[
            urlsafe_base64_encode(force_bytes(self.object.pk)),
            accountActivationToken.make_token(self.object)
        ])
        self.object.email_user(
            subject=mailSubject,
            message=f'''Ciao {self.object.username}, e benvenuto sul nostro portale turistico! Clicca il link seguente per confermare il tuo account:\n{self.request.build_absolute_uri(confirmUrl)}\nA presto'''
        )
        self.object.token_sent = True
        self.object.is_active = False
        self.object.save()

        return response


def userLoginByToken(request, user_id_b64=None, user_token=None):
    try:
        uid = force_text(urlsafe_base64_decode(user_id_b64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and accountActivationToken.check_token(user, user_token):
        user.is_active = True
        user.save()
        login(request, user)
        return True

    return False


def verifyUserEmail(request, user_id_b64=None, user_token=None):
    if not userLoginByToken(request, user_id_b64, user_token):
        message = "Errore: Tentativo di validazione email per l'utente {user} con token {token}"
        # TODO log it

    return redirect('login')


def confirmRegistration(request):
    return render(request, 'registration/confirmRegistration.html')


class UpdateUserSettings(UpdateView):
    model = User
    template_name = 'updateSettings.html'
    form_class = UpdateUserSettingsForm

    def form_valid(self, form):
        response = super(UpdateUserSettings, self).form_valid(form)
        messages.success(self.request, "Informazioni salvate correttamente")
        return response

    def get_success_url(self):
        return reverse('userSettings', kwargs={'pk': self.request.user.pk})
