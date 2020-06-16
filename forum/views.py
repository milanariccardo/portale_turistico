from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from forum.models import Category, Thread, Comment
from userManagement.models import Profile


class MainPageForum(ListView):
    model = Category
    template_name = "mainPageForum.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageForum, self).get_context_data()
        d = {}
        # Crea un dizionario del tipo {category: numero_thread_attivi}
        for cat in self.object_list:
            t = Thread.objects.filter(category=cat) & Thread.objects.filter(is_active=True)
            d[cat] = t.count()
        context['category'] = d


        return context


class CreateCategoryForum(CreateView):
    model = Category
    template_name = "createCategoryForum.html"
    fields = '__all__'
    success_url = reverse_lazy('mainPageCategory')


class UpdateCategoryForum(UpdateView):
    model = Category
    template_name = "updateCategoryForum.html"
    fields = '__all__'
    success_url = reverse_lazy('mainPageCategory')

    def form_valid(self, form):
        response = super(UpdateCategoryForum, self).form_valid(form)
        messages.success(self.request, "Categoria modificata correttamente")
        return super(UpdateCategoryForum, self).form_valid(form)




class ViewThreadCategoryForum(ListView):
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


class CreateThreadForum(CreateView):
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


def delete_thread(request, **kwargs):
    print(kwargs['pk_thread'])
    # image = ListPhoto.objects.get(pk=kwargs['pk'])
    # image.delete()
    # messages.success(request, "Rimozione effettuata correttamente")
    # print(kwargs['pk1'])
    # print(kwargs['pk2'])
    # return redirect(reverse('editReview', kwargs={'pk1': kwargs['pk1'], 'pk2': kwargs['pk2']}))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ViewThreadCommentForum(DetailView):
    model = Thread
    template_name = 'viewThreadCommentForum.html'
    pk_url_kwarg = "pk_thread"

    def get_context_data(self, **kwargs):
        # Ritorna tutti i commenti relativi al thread in ordine temporale
        print(self.object)
        context = super().get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(thread=self.object).order_by('created_at')

        # Ritorna la categoria del thread
        context['category'] = Category.objects.filter(pk=self.kwargs.get('pk_category')).last()
        return context


class CreateCommentThreadForum(CreateView):
    model = Comment
    template_name = "createThreadForum.html"
    # success_url = reverse_lazy('mainPageCategory')
    fields = ['text']

    def form_valid(self, form):
        # Ottieni il profilo dell'utente attuale
        profile = Profile.objects.filter(user__username=self.request.user).last()

        # Ottini il thread in cui è contenuto il commento
        thread = Thread.objects.filter(pk=self.kwargs.get('pk_thread')).last()

        form.instance.user = profile
        form.instance.thread = thread

        return super(CreateCommentThreadForum, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('viewThreadComment', kwargs={'pk_category': self.kwargs.get('pk_category'),
                                                         'pk_thread': self.kwargs.get('pk_thread')})


# Blocca il thread
def lockThread(request, pk_category, pk_thread):
    # Recupero il Thread e lo blocco
    t = Thread.objects.filter(pk=pk_thread).last()
    t.is_active = False
    print(t)
    print(t.is_active)
    try:
        t.save()
        messages.success(request, 'Thread bloccato!')
    except:
        pass
    #Ritorna all'url precedente (quello dei thread)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
