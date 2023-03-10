from django.urls import path, include
from django.contrib.auth import views as auth_view
from . import views
from .views import Registration, UpdateUserSettings

urlpatterns = [
    path('signup/', Registration.as_view(), name='registration'),
    path('verify/<str:user_id_b64>/<str:user_token>', views.verifyUserEmail, name='verifyUserEmail'),
    path('registration/confirm/', views.confirmRegistration, name='confirmRegistration'),
    # path('user_settings/<int:pk>/', UpdateUserSettings.as_view(), name='userSettings'),
    path('user_settings/', UpdateUserSettings.as_view(), name='userSettings'),
    path('password/', views.change_password, name='change_password'),
    path('remove_account/', views.removeAccount, name='removeAccount'),

    # Path per il reset della password
    path('reset_password/', auth_view.PasswordResetView.as_view(template_name="registration/passwordReset.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_view.PasswordResetDoneView.as_view(template_name="registration/passwordResetDone.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_view.PasswordResetConfirmView.as_view(template_name="registration/passwordResetConfirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name="registration/passwordResetComplete.html"),
         name='password_reset_complete'),
]
