from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView

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