from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from pathManagement.forms import InsertPathForm
from pathManagement.models import Path


class InsertPath(CreateView):
    model = Path
    template_name = 'insertPath.html'
    form_class = InsertPathForm

    def form_valid(self, form):
        response = super(InsertPath, self).form_valid(form)
        messages.success(self.request, "Percorso inserito correttamente")
        return response

    def get_success_url(self):
        return reverse('insertPath')


class ShowPath(ListView):
    model = Path
    template_name = 'showPath.html'


def removePath(request, id):
    path = Path.objects.get(id=id)
    path.delete()
    messages.success(request, "Percorso eliminato con successo")

    return reverse_lazy(request, 'showPath.html')
