from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.core.exceptions import RequestAborted
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from forum.models import Category, Thread, Comment
from userManagement.models import Profile

from braces import views as bc


# Metodo che ritorna True se l'utente che ha effettuato la richiesta è amministratore o ha creato l'oggetto object
def get_permission(request, object_user_pk):
    print(request.user.pk)
    print(object_user_pk)
    if request.user.is_staff:
        return True
    else:
        return True if object_user_pk == request.user.pk else False


# ok
class MainPageForum(bc.LoginRequiredMixin, ListView):
    model = Category
    template_name = "mainPageForum.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageForum, self).get_context_data()
        d = {}
        # Crea un dizionario del tipo {category: numero_thread_attivi}
        for cat in self.object_list:
            t = Thread.objects.filter(category=cat)
            d[cat] = t.count()
        context['category'] = d

        return context


# ok
class CreateCategoryForum(bc.StaffuserRequiredMixin, CreateView):
    model = Category
    template_name = "createCategoryForum.html"
    fields = '__all__'
    success_url = reverse_lazy('mainPageCategory')


# ok
class UpdateCategoryForum(bc.StaffuserRequiredMixin, UpdateView):
    model = Category
    template_name = "updateCategoryForum.html"
    fields = '__all__'
    success_url = reverse_lazy('mainPageCategory')

    def form_valid(self, form):
        response = super(UpdateCategoryForum, self).form_valid(form)
        messages.success(self.request, "Categoria modificata correttamente")
        return super(UpdateCategoryForum, self).form_valid(form)


# ok
class ViewThreadCategoryForum(bc.LoginRequiredMixin, ListView):
    model = Thread
    template_name = "viewThreadForum.html"

    def get_context_data(self, **kwargs):
        context = super(ViewThreadCategoryForum, self).get_context_data()
        d = {}
        # Creazione di un dizionario del tipo {thread: num_risposte}
        for th in Thread.objects.filter(category=self.kwargs.get('pk')):
            d[th] = Comment.objects.filter(thread=th).count()
        context['thread'] = d
        context['category'] = Category.objects.filter(pk=self.kwargs.get('pk')).last()

        return context


# ok
class CreateThreadForum(bc.LoginRequiredMixin, CreateView):
    model = Thread
    template_name = "createThreadForum.html"
    fields = ['title', 'text']
    success_url = reverse_lazy('mainPageCategory')

    def get_success_url(self):
        # Ritorna all'url precedente (quello dei thread)
        return reverse_lazy('viewThreadCategory', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(CreateThreadForum, self).get_context_data()
        context['category'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Ottieni il profilo dell'utente attuale
        profile = Profile.objects.filter(user__username=self.request.user).last()

        # Ottini la categoria in cui si sta creando il thread
        category = Category.objects.filter(pk=self.kwargs.get('pk')).last()

        form.instance.user = profile
        form.instance.category = category

        response = super(CreateThreadForum, self).form_valid(form)
        messages.success(self.request, "Thread creato correttamente")

        return super(CreateThreadForum, self).form_valid(form)


# ok
class ViewThreadCommentForum(bc.LoginRequiredMixin, DetailView):
    model = Thread
    template_name = 'viewThreadCommentForum.html'
    pk_url_kwarg = "pk_thread"

    def get_context_data(self, **kwargs):
        # Ritorna tutti i commenti relativi al thread in ordine temporale
        context = super().get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(thread=self.object).order_by('created_at')

        # Ritorna la categoria del thread
        context['category'] = Category.objects.filter(pk=self.kwargs.get('pk_category')).last()
        return context


# ok
class CreateCommentThreadForum(bc.LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "createCommentForum.html"
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ottini il thread in cui è contenuto il commento
        thread = Thread.objects.filter(pk=self.kwargs.get('pk_thread')).last()

        context['thread_lock'] = True if thread.is_active else False

        return context

    def get(self, request, *args, **kwargs):
        thread = Thread.objects.filter(pk=self.kwargs.get('pk_thread')).last()
        if thread.is_active:
            return super(CreateCommentThreadForum, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        # Ottieni il profilo dell'utente attuale
        profile = Profile.objects.filter(user__username=self.request.user).last()

        # Ottini il thread in cui è contenuto il commento
        thread = Thread.objects.filter(pk=self.kwargs.get('pk_thread')).last()

        form.instance.user = profile
        form.instance.thread = thread

        messages.success(self.request, "Commento inserito correttamente")

        return super(CreateCommentThreadForum, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('viewThreadComment', kwargs={'pk_category': self.kwargs.get('pk_category'),
                                                         'pk_thread': self.kwargs.get('pk_thread')})


#Elimina la categoria
@staff_member_required
def delete_category(request, **kwargs):
    try:
        Category.objects.filter(pk=kwargs['pk']).last().delete()
        messages.success(request, 'Categoria eliminata')
    except:
        print("Impossibile eliminare la categoria!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Blocca il thread
@staff_member_required
def lockThread(request, pk_category, pk_thread):
    # Recupero il Thread e lo blocco
    t = Thread.objects.filter(pk=pk_thread).last()
    t.is_active = False
    try:
        t.save()
        messages.success(request, 'Thread bloccato!')
    except:
        pass
    # Ritorna all'url precedente (quello dei thread)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Sblocca il thread
@staff_member_required
def unlockThread(request, pk_category, pk_thread):
    # Recupero il Thread
    t = Thread.objects.filter(pk=pk_thread).last()
    # Se il thread è bloccato
    if not t.is_active:
        t.is_active = True
    else:
        messages.error(request, 'Il thread era già sbloccato!', extra_tags='thread_unlock_error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    try:
        t.save()
        messages.success(request, 'Thread sbloccato!')
    except:
        pass

    # Ritorna all'url precedente (quello dei thread)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Elimina il thread
@staff_member_required
def delete_thread(request, **kwargs):
    try:
        Thread.objects.filter(pk=kwargs['pk_thread']).last().delete()
        messages.success(request, 'Thread eliminato!')
    except:
        print("Impossibile eliminare thread!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Modifica Commento
class EditCommentForum(bc.LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "editCommentForum.html"
    fields = ['text']
    success_url = reverse_lazy('mainPageCategory')
    pk_url_kwarg = "pk_comment"

    def get(self, request, *args, **kwargs):
        # Ottengo il commento corrente
        var = Comment.objects.filter(pk=self.kwargs['pk_comment']).last()

        # Ottengo l'utente associato al profilo che ha creato il commento
        user = Profile.objects.filter(pk=var.user.pk).values('user').last()

        # Se sono l'utente che ha creato il commento (o parte dello staff) e il thread è ancora aperto
        if get_permission(self.request, user['user']) & \
                Thread.objects.filter(pk=var.thread.pk).values('is_active').last()['is_active']:
            return super(EditCommentForum, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.is_modified = True
        messages.success(self.request, "Commento modificato correttamente")
        return super(EditCommentForum, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('viewThreadComment', kwargs={'pk_category': self.kwargs.get('pk_category'),
                                                         'pk_thread': self.kwargs.get('pk_thread')})


# Elimina Commento
@staff_member_required
def delete_comment(request, **kwargs):
    # Ottengo il commento corrente
    var = Comment.objects.filter(pk=kwargs['pk_comment']).last()

    # Ottengo l'utente associato al profilo che ha creato il commento
    user = Profile.objects.filter(pk=var.user.pk).values('user').last()

    # Se il thread è ancora aperto
    if Thread.objects.filter(pk=var.thread.pk).values('is_active').last()['is_active']:
        try:
            Comment.objects.filter(pk=kwargs['pk_comment']).last().delete()
            messages.success(request, 'Commento eliminato!')
        except:
            print("Impossibile eliminare commento!")
    else:
        raise PermissionDenied

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
