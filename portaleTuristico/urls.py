import os

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from portaleTuristico import views
from django.conf import settings
from django.conf.urls.static import static

from userManagement.views import UpdateUserSettings, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.homepage, name='homepage'),
    path('accounts/', include('userManagement.urls')),
    path('path/', include('pathManagement.urls')),
    path('user_settings/<int:pk>/', UpdateUserSettings.as_view(), name='userSettings'),
    path('password/', change_password, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
