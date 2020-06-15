from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from forum.models import Category, Thread


class MainPageForum(ListView):
    model = Category
    template_name = "mainPageForum.html"

class CreateCategoryForum(CreateView):
    model = Category
    template_name = "createCategoryForum.html"
    fields = '__all__'
    success_url = reverse_lazy('mainPageCategory')

class UpdateCategoryForum(UpdateView):
    model = Category
    template_name = "updateCategoryForum.html"

# Delete
### def()


class ViewThreadForum(ListView):
    model = Thread
    template_name = "viewThreadForum.html"