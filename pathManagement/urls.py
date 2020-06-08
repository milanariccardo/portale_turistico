from django.contrib import admin
from django.urls import path, include

from pathManagement.views import InsertPath

urlpatterns = [
    path('insert/', InsertPath.as_view(), name='insertPath'),
]
