from django.urls import path, include
from . import views
from .views import Registration

urlpatterns = [
    path('signup/', Registration.as_view(), name='registration'),
    path('verify/<str:user_id_b64>/<str:user_token>', views.verifyUserEmail, name='verifyUserEmail'),
    # path('registration/confirm/', views.registrationSuccess, name='registrationSuccess'),
]
