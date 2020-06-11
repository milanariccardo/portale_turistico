from django.contrib import admin
from django.urls import path, include

from pathManagement.views import InsertPath, ShowPath, EditPath, DetailPath, InsertPathReview
from .views import removePath, searchPath

urlpatterns = [
    path('insert/', InsertPath.as_view(), name='insertPath'),
    path('edit/<int:pk>/', EditPath.as_view(), name='editPath'),
    path('show/', ShowPath.as_view(), name='showPath'),
    path('delete/<int:pk>', removePath, name='removePath'),
    path('search/', searchPath, name='searchPath'),
    path('detail/<int:pk>/', DetailPath.as_view(), name='detailPath'),
    path('review/<int:pk1>-<int:pk2>/', InsertPathReview.as_view(), name='insertReview')
]
