from django.contrib import admin
from django.urls import path, include

from pathManagement.views import InsertPath, ShowPath, removePath
from . import views

urlpatterns = [
    path('insert/', InsertPath.as_view(), name='insertPath'),
    path('show/', ShowPath.as_view(), name='showPath'),
    path('delete/<int:id>', views.removePath, name='removePath'),
]
