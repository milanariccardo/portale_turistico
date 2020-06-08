from django.shortcuts import render
from django.views.generic import CreateView
from pathManagement.models import Path


class InsertPath(CreateView):
    model = Path
    template_name = 'insertPath.html'
    fields = '__all__'
