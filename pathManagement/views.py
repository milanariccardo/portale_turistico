import os
from braces import views as bc
import pandas as pd

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from pathManagement.filters import PathFilter
from pathManagement.forms import InsertPathForm, EditPathForm, InsertPathReviewForm, EditPathReviewForm
from pathManagement.models import Path, Review, ListPhoto
from userManagement.models import Profile

from recommendation.recommendation import MatrixPathFeature

from forum.views import get_permission


## Funzione che ritorna la review di una coppia (path.id, utente.id)
def return_review(pk_path, pk_user):
    path = Path.objects.filter(id=pk_path).last()
    user = User.objects.filter(pk=pk_user).last()
    profile = Profile.objects.filter(user=user).last()
    return Review.objects.filter(user=profile, path=path).last()


# Ok
class InsertPath(bc.StaffuserRequiredMixin, CreateView):
    model = Path
    template_name = 'insertPath.html'
    form_class = InsertPathForm

    def form_valid(self, form):
        response = super(InsertPath, self).form_valid(form)
        messages.success(self.request, "Percorso inserito correttamente")

        # Aggiorna la matrice di similarità
        update_matrix = MatrixPathFeature()

        return response

    def get_success_url(self):
        return reverse_lazy('showPath')


# Ok
class EditPath(bc.StaffuserRequiredMixin, UpdateView):
    model = Path
    template_name = 'modifyPath.html'
    form_class = EditPathForm

    def form_valid(self, form):
        response = super(EditPath, self).form_valid(form)
        messages.success(self.request, "Informazioni modificate correttamente")

        # Aggiorna la matrice di similarità
        update_matrix = MatrixPathFeature()

        return response

    def get_success_url(self):
        return reverse_lazy('showPath')


# Ok
class ShowPath(bc.StaffuserRequiredMixin, ListView):
    model = Path
    template_name = 'showPath.html'


# Ok
@staff_member_required
def removePath(request, pk):
    path = Path.objects.get(id=pk)
    path.delete()
    messages.success(request, "Percorso eliminato con successo")

    # Aggiorna la matrice di similarità
    if not Path.objects.all():
        try:
            os.remove(os.path.join(os.getcwd(), 'matrix'))
        except:
            print("Impossibile eliminare il file")
    else:
        update_matrix = MatrixPathFeature()

    return redirect('showPath')


# Ok
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
            messages.error(request, "I kilometri minimi non possono essere maggiori dei kilometri massimi!")
            path_list = Path.objects.none()

    path_filter = PathFilter(request.GET, queryset=path_list)
    dict_num_review = {}
    review = {}

    for path in path_filter.qs:
        review[path.pk] = 0
        val = Review.objects.filter(path=path).values('valuation')
        iteration = val.count()
        dict_num_review[path.pk] = iteration

        for i in val:
            review[path.pk] = review[path.pk] + i['valuation'] / iteration

    return render(request, 'searchPath.html', {'filter': path_filter, 'review': review, 'num_review': dict_num_review})


# Ok
class DetailPath(DetailView):
    model = Path
    template_name = 'detailPath.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailPath, self).get_context_data()

        # Creazione del contesto relativo alle recensioni
        context['review'] = Review.objects.filter(path=self.object)

        # Dizionario che sarà passato come set di dati per la creazione del grafico
        review_data = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}
        # Dizionario che conterrà le immagini inserite nelle review dagli utenti
        photo_review = {}

        for image in context['review']:
            photo_review[image] = ListPhoto.objects.filter(review=image)
            review_data[str(image.valuation)] = review_data[str(image.valuation)] + 1

        context['chart_data'] = review_data
        context['list_photo'] = photo_review

        path_review = Review.objects.filter(path=self.object.id).values('valuation')

        iteration = path_review.count()
        count = 0

        for value in path_review:
            count = count + value['valuation'] / iteration

        # Contesto per la media delle recensioni
        context['valuation'] = count

        # Contesto per il numero di persone che hanno recensito il percorso
        context['people'] = iteration

        # Ottieni la matrice di similarità e i percorsi consigliati
        recommendation = []
        if os.path.join(os.getcwd(), 'matrix'):
            try:
                # Leggi il file matrix
                matrix = pd.read_csv(os.path.join(os.getcwd(), 'matrix'), index_col=0)
                # Ottieni la riga relativa al path corrente e riordinala in ordine decrescente di similarità
                row_path = matrix.loc[self.object.pk].sort_values(ascending=False)
                # Restituisci i primi cinque risultati
                recommendation = list(row_path.axes[0])[1:5]
                recommendation = [int(x) for x in recommendation]
            except:
                print("La matrice non esiste")

        # Creazione contesto recommandations
        # Questa parte di view crea un dizionario del tipo {'PathObject(n)': [valutazione_media, numero_voti]}
        # per essere successivamente passato come contesto
        recommendation_context = {}
        average_review = 0


        for r in recommendation:
            recommendation_review = Review.objects.filter(path__id=r).values('valuation')
            num_path = recommendation_review.count()

            for value in recommendation_review:
                average_review = average_review + value['valuation'] / num_path
            recommendation_context[Path.objects.filter(id=r).last()] = [average_review, num_path]
            average_review = 0
        context['recommendation_context'] = recommendation_context

        # Creazione contesto percorsi composti
        # Questa parte di view crea un dizionario del tipo {'<PathObject(n)>': [valutazione_media, numero_voti]}
        # per essere successivamente passato come contesto
        compound_path_context = {}
        average_compound_path_review = 0


        # Recupero percorsi composti
        # Se il percorso non è un anello restitituisci i percorsi composti
        if self.object.start != self.object.end:
            compound_path = Path.objects.filter(start=self.object.end) & Path.objects.filter(activity=self.object.activity)
            for cp in compound_path:
                compound_path_review = Review.objects.filter(path=cp).values('valuation')
                num_compound_path = compound_path_review.count()

                # Calcolo valutazione media
                for value in compound_path_review:
                    average_compound_path_review = average_compound_path_review + value['valuation'] / num_compound_path
                compound_path_context[cp] = [average_compound_path_review, num_compound_path]
                average_compound_path_review = 0
        else:
            compound_path = {}
        context['compound_path'] = compound_path_context
        return context


# Ok
class InsertPathReview(bc.LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'insertPathReview.html'
    form_class = InsertPathReviewForm

    def get_initial(self):
        initial = super().get_initial()
        initial['pk1'] = self.kwargs.get('pk1')
        initial['pk2'] = self.kwargs.get('pk2')
        return initial

    def form_valid(self, form):
        response = super(InsertPathReview, self).form_valid(form)
        messages.success(self.request, "Recensione inserita correttamente")
        return response

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        instance = form.save()

        if form.is_valid():
            for f in files:
                ListPhoto.objects.create(review=instance, photo=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('detailPath', kwargs={'pk': self.kwargs.get('pk2')})


# Ok
class EditPathReview(bc.LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'editPathReview.html'
    form_class = EditPathReviewForm

    def get(self, request, *args, **kwargs):
        # Ottengo la review corrente
        var = Review.objects.filter(path__id=self.kwargs['pk2']).last() and Review.objects.filter(
            user__id=self.kwargs['pk1']).last()

        # Ottengo l'utente associato al profilo che ha creato la review
        user = Profile.objects.filter(pk=var.user.pk).values('user').last()

        # Se sono l'utente che ha creato il commento (o parte dello staff)
        if get_permission(self.request, user['user']):
            return super(EditPathReview, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self, queryset=None):
        return return_review(self.kwargs.get('pk2'), self.kwargs.get('pk1'))

    def get_context_data(self, **kwargs):
        context = super(EditPathReview, self).get_context_data()
        review = return_review(self.kwargs.get('pk2'), self.kwargs.get('pk1'))
        image = ListPhoto.objects.filter(review=review)
        context['image'] = image
        context['pk_user'] = self.kwargs.get('pk1')
        context['pk_path'] = self.kwargs.get('pk2')
        return context

    def post(self, request, *args, **kwargs):
        super(EditPathReview, self).post(request, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        review = return_review(self.kwargs.get('pk2'), self.kwargs.get('pk1'))
        if form.is_valid():
            messages.success(self.request, "Informazioni modificate correttamente")
            for f in files:
                ListPhoto.objects.create(review=review, photo=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('detailPath', kwargs={'pk': self.kwargs.get('pk2')})


# Ok
@login_required
def delete_review(request, **kwargs):
    # Ottengo la review corrente
    var = Review.objects.filter(path__id=kwargs['pk2']).last() and Review.objects.filter(
        user__id=kwargs['pk1']).last()

    # Ottengo l'utente associato al profilo che ha creato la review
    user = Profile.objects.filter(pk=var.user.pk).values('user').last()
    if get_permission(request, user['user']):
        review = Review.objects.get(user__id=kwargs['pk1'], path__id=kwargs['pk2'])
        reviewPhoto = ListPhoto.objects.filter(review=review)
        reviewPhoto.delete()
        review.delete()
        messages.success(request, "Rimozione della recensione effettuata correttamente")
        return redirect(reverse('detailPath', kwargs={'pk': kwargs['pk2']}))
    else:
        raise PermissionDenied


# Ok
@login_required
def delete_image_review(request, **kwargs):
    # Ottengo la review corrente
    var = Review.objects.filter(path__id=kwargs['pk2']).last() and Review.objects.filter(
        user__id=kwargs['pk1']).last()

    # Ottengo l'utente associato al profilo che ha creato la review
    user = Profile.objects.filter(pk=var.user.pk).values('user').last()
    if get_permission(request, user['user']):
        image = ListPhoto.objects.get(pk=kwargs['pk'])
        image.delete()
        messages.success(request, "Rimozione effettuata correttamente")
        return redirect(reverse('editReview', kwargs={'pk1': kwargs['pk1'], 'pk2': kwargs['pk2']}))
    else:
        raise PermissionDenied
