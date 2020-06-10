from django.contrib import admin
from django.urls import path, include

from pathManagement.views import InsertPath, ShowPath, EditPath
from .views import removePath, searchPath

urlpatterns = [
    path('insert/', InsertPath.as_view(), name='insertPath'),
    path('edit/<int:pk>/', EditPath.as_view(), name='editPath'),
    path('show/', ShowPath.as_view(), name='showPath'),
    path('delete/<int:pk>', removePath, name='removePath'),
    path('search/', searchPath, name='searchPath'),
]
