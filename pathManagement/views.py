from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from pathManagement.filters import PathFilter
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


def searchPath(request):
    km_max = request.GET.get('km_max')
    km_min = request.GET.get('km_min')

    path_list = Path.objects.all()

    if km_max and float(km_max) <= 0:
        messages.error(request, "Valore di km massimo non accettato")
        path_list = Path.objects.none()

    if km_min and float(km_min) <= 0:
        messages.error(request, "Valore di km minimoadd icon  non accettato")
        path_list = Path.objects.none()

    if km_min and km_max:
        if float(km_min) > float(km_max):
            messages.error(request, "Il kilometri minimi non possono essere maggiori dei kilometri massimi!")
            path_list = Path.objects.none()

    path_filter = PathFilter(request.GET, queryset=path_list)
    return render(request, 'searchPath.html', {'filter': path_filter})
