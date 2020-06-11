from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from pathManagement.filters import PathFilter
from pathManagement.forms import InsertPathForm, EditPathForm
from pathManagement.models import Path, Review


class InsertPath(CreateView):
    model = Path
    template_name = 'insertPath.html'
    form_class = InsertPathForm

    def form_valid(self, form):
        response = super(InsertPath, self).form_valid(form)
        messages.success(self.request, "Percorso inserito correttamente")
        return response

    def get_success_url(self):
        return reverse_lazy('showPath')


class EditPath(UpdateView):
    model = Path
    template_name = 'modifyPath.html'
    form_class = EditPathForm

    def form_valid(self, form):
        response = super(EditPath, self).form_valid(form)
        messages.success(self.request, "Informazioni modificate correttamente")
        return response

    def get_success_url(self):
        return reverse_lazy('showPath')


class ShowPath(ListView):
    model = Path
    template_name = 'showPath.html'


def removePath(request, pk):
    path = Path.objects.get(id=pk)
    path.delete()
    messages.success(request, "Percorso eliminato con successo")
    return redirect('showPath')


def searchPath(request):
    km_max = request.GET.get('km_max')
    km_min = request.GET.get('km_min')

    path_list = Path.objects.all()

    if km_max and float(km_max) <= 0:
        messages.error(request, "Valore di km massimo non accettato")
        path_list = Path.objects.none()

    if km_min and float(km_min) <= 0:
        messages.error(request, "Valore di km minimo non accettato")
        path_list = Path.objects.none()

    if km_min and km_max:
        if float(km_min) > float(km_max):
            messages.error(request, "Il kilometri minimi non possono essere maggiori dei kilometri massimi!")
            path_list = Path.objects.none()

    path_filter = PathFilter(request.GET, queryset=path_list)
    review = {}

    for path in path_filter.qs:
        review[path.pk] = 0
        val = Review.objects.filter(path=path).values('valuation')
        iteration = val.count()
        for i in val:
            review[path.pk] = review[path.pk] + i['valuation'] / iteration
    return render(request, 'searchPath.html', {'filter': path_filter, 'review': review})

class DetailPath(DetailView):
    model = Path
    template_name = 'detailPath.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailPath, self).get_context_data()
        context['review'] = Review.objects.filter(path=self.object)
        path_review = Review.objects.filter(path=self.object.id).values('valuation')
        iteration = path_review.count()
        count = 0
        for value in path_review:
            print(value['valuation'])
            count = count + value['valuation'] / iteration
        print(count)
        context['valuation'] = count
        return context
