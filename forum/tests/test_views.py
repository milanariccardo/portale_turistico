import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from forum.models import Category, Thread, Comment


class TestView(TestCase):
    """Classe che verifica il corretto funzionamento delle viste utente"""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
                viene creato uno user che verrà utilizzato nel corso del test"""

        # Reverse per la view di mainPageForum (homePage del Forum)
        self.mainPageCategory = reverse('mainPageCategory')

        # Reverse per la view di CreateCategoryForumLogged (pagina di creazione di una categoria)
        self.CreateCategoryForumLogged = reverse('createCategory')

        # Reverse per la view di UpdateCategoryForum (pagina di modifica di una categoria)
        self.CreateCategoryForumLogged = reverse('editCategory', args=['1'])

        # Reverse per la view di ViewThreadCategoryForum (pagina di visualizzazione dei thread di una categoria)
        self.ViewThreadCategoryForum = reverse('viewThreadCategory', args=['1'])

        # Reverse per la view di CreateThreadForum(pagina di creazione di un thread)
        self.CreateThreadForum = reverse('createThread', args=['1'])

        # Reverse per la view di ViewThreadCommentForum (pagina di visualizzazione dei commenti relativi a un thread)
        self.ViewThreadCommentForum = reverse('viewThreadComment', args=['1', '1'])

        # Reverse per la view di CreateCommentThreadForum(pagina di creazione di un commento in un thread)
        self.CreateCommentThreadForum = reverse('createComment', args=['1', '1'])

        # Reverse per la view di lockThread (url che permette di bloccare le risposte di un thread)
        self.lockThread = reverse('lockThread', args=['1', '1'])

        # Reverse per la view di delete_thread (url che permette di eliminare un thread)
        self.delete_thread = reverse('deleteThread', args=['1', '1'])

        # Reverse per la view di delete_comment (url che permette di eliminare un messaggio nel thread)
        self.delete_comment = reverse('deleteComment', args=['1', '1', '1'])

        # Creazione categoria
        self.category1 = Category.objects.create(title="Walk")

        # Creazione utente
        self.user = User.objects.create(username='testuser', email="testUser@test.com")
        self.user.set_password('password')
        self.user.save()

        # Creazione utente dello staff
        self.userStaff = User.objects.create(username='userStaff', email="userStaff@test.com")
        self.userStaff.set_password('password')
        self.userStaff.is_staff = True
        self.userStaff.save()

        # Creazione di un thread nella categoria Walk
        self.thread1 = Thread.objects.create(title="ThreadWalk", text="Test", category=self.category1,
                                             user=self.user.profile)

        # Creazione di un commento nel thread ThreadWalk
        self.comment1 = Comment.objects.create(text="Test", thread=self.thread1,
                                               user=self.user.profile)

        self.client = Client()

    def testMainPageForumLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di Home del Forum sia 200 (buon fine), nel caso l'utente sia loggato. Inoltre controlla che il contesto contenga la categoria creata e il numero di thread per categoria corretti"""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.mainPageCategory)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category_list'].last().title, self.category1.title)
        # Si assume che sia stata inserita una sola categoria -> ritorna 1, ovvero il numero di Thread presenti in category1
        self.assertEqual(list(response.context['category'].values())[0], 1)

    def testMainPageForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di Home del Forum sia 302 (redirect), nel caso l'utente sia non loggato. """

        response = self.client.get(self.mainPageCategory)
        self.assertEqual(response.status_code, 302)

    def testCreateCategoryForumLoggedStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di creazione di una categoria sia 200 (buon fine), nel caso in cui l'utente loggato sia parte dello staff."""

        self.client.login(username='userStaff', password='password')
        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 200)

    def testCreateCategoryForumLoggedNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di creazione di una categoria sia 302 (Redirect), nel caso in cui l'utente loggato non sia parte dello staff."""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 302)

    def testCreateCategoryForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di creazione di una categoria sia 302 (Redirect), nel caso in cui l'utente non sia loggato"""

        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 302)

    def testUpdateCategoryForumLoggedStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                       della pagina di modifica di una categoria sia 200 (buon fine), nel caso in cui l'utente loggato sia parte dello staff."""

        self.client.login(username='userStaff', password='password')
        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 200)

    def testUpdateCategoryForumLoggedNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                       della pagina di modifica di una categoria sia 302 (redirect), nel caso in cui l'utente loggato non sia parte dello staff."""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 302)

    def testUpdateCategoryForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                       della pagina di modifica di una categoria sia 302 (redirect), nel caso in cui l'utente non sia loggato """

        response = self.client.get(self.CreateCategoryForumLogged)
        self.assertEqual(response.status_code, 302)

    def testViewThreadCategoryForumLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                       della pagina di visione dei thread di una categoria sia 200 (buon fine), nel caso l'utente sia loggato. Inoltre controlla che il contesto contenga il thread creato all'interno della category1 e il numero di risposte per il thread sia corretto"""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.ViewThreadCategoryForum)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['thread_list'].last().title, self.thread1.title)
        # Si assume che sia stata inserita una solo thread -> ritorna 1, ovvero il numero di commenti presenti in thread1
        self.assertEqual(list(response.context['thread'].values())[0], 1)

    def testViewThreadCategoryForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                       della pagina di visione dei thread di una categoria sia 302 (redirect), nel caso l'utente non sia loggato. """

        response = self.client.get(self.ViewThreadCategoryForum)
        self.assertEqual(response.status_code, 302)

    def testCreateThreadForumLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                               della pagina di creazione di un thread sia 200 (buon fine), nel caso l'utente sia loggato."""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.CreateThreadForum)
        self.assertEqual(response.status_code, 200)

    def testCreateThreadForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                               della pagina di creazione di un thread sia 302 (redirect), nel caso l'utente non sia loggato."""

        response = self.client.get(self.CreateThreadForum)
        self.assertEqual(response.status_code, 302)

    def testViewThreadCommentForumLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                      della pagina di visualizzazione dei commenti di un thread sia 200 (buon fine), nel caso l'utente sia loggato. Inoltre controlla che i commenti vengano mostrati in ordine cronologico."""

        self.client.login(username='testuser', password='password')

        # Creazione di un secondo commento nel thread ThreadWalk, con data di creazione maggiore
        time = timezone.now() + datetime.timedelta(days=30)
        self.comment2 = Comment.objects.create(text="Test2", thread=self.thread1,
                                               user=self.userStaff.profile)
        self.comment2.created_at = time
        self.comment2.save()

        response = self.client.get(self.ViewThreadCommentForum)
        self.assertEqual(response.status_code, 200)

        # Controlla che il contesto sia ordinato
        self.assertEqual(response.context['comment'][0].created_at < response.context['comment'][1].created_at, True)

        # Controlla che la categoria dei commenti sia Walk, cioè quella del thread in cui sono stati creati
        self.assertEqual(response.context['category'].title, "Walk")

        self.comment2.delete()

    def testViewThreadCommentForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                      della visualizzazione dei commenti di un thread sia 302 (redirect), nel caso l'utente non sia loggato."""

        response = self.client.get(self.ViewThreadCommentForum)
        self.assertEqual(response.status_code, 302)

    def testdelete_categoryLoginStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                             della pagina di eliminazione di una categoria sia 302 (ricarica la HomePage del Forum), nel caso in cui l'utente loggato sia parte dello staff."""

        self.client.login(username='userStaff', password='password')

        # Creo una categoria da eliminare
        self.category2 = Category.objects.create(title="Remove")

        self.delete_category = reverse('deleteCategory', args=[self.category2.pk])
        response = self.client.get(self.delete_category)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Controlla che la categoria è stata eliminata
        self.assertEqual(Category.objects.filter(title="Remove").count(), 0)

    def testdelete_categoryLoginNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                             della pagina di eliminazione di una categoria sia 302 (redirect alla pagina di login di admin), nel caso in cui l'utente loggato  non sia parte dello staff."""

        self.client.login(username='testuser', password='password')
        self.delete_category = reverse('deleteCategory', args=['1'])
        response = self.client.get(self.delete_category)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual('admin/login' in response.url, True)

    def testdelete_categoryNoLogin(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                             della pagina di eliminazione di una categoria sia 302 (redirect alla pagina di login di admin), nel caso in cui l'utente non sia loggato."""

        self.delete_category = reverse('deleteCategory', args=['1'])
        response = self.client.get(self.delete_category)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual('admin/login' in response.url, True)

    def testunlockThreadLoginStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                     della pagina per sbloccare un thread sia 302 (ricarica la pagina dei thread di una categoria), nel caso in cui l'utente loggato sia parte dello staff."""

        self.client.login(username='userStaff', password='password')

        # Creo un thread bloccato
        self.thread2 = Thread.objects.create(title="Thread2", text="Test", category=self.category1,
                                             user=self.user.profile, is_active=False)

        self.unlockThread = reverse('unlockThread', args=['1', self.thread2.pk])
        response = self.client.get(self.unlockThread)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Controlla che la il thread sia stato sbloccato
        self.assertEqual(Thread.objects.filter(pk=self.thread2.pk).last().is_active, True)

    def testunlockThreadLoginNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                     della pagina per sbloccare un thread sia 302 (redirect alla pagina di login di admin), nel caso in cui l'utente loggato non sia parte dello staff."""

        self.client.login(username='testuser', password='password')

        self.unlockThread = reverse('unlockThread', args=['1', self.thread1.pk])
        response = self.client.get(self.unlockThread)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual('admin/login' in response.url, True)

    def testunlockThreadNoLogin(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                     della pagina per sbloccare un thread sia 302 (redirect alla pagina di login di admin), nel caso in cui l'utente non sia loggato"""

        self.unlockThread = reverse('unlockThread', args=['1', self.thread1.pk])
        response = self.client.get(self.unlockThread)

        # Controlla che il redirect sia corretto
        self.assertEqual(response.status_code, 302)
        self.assertEqual('admin/login' in response.url, True)

    def testEditCommentForumLogin(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                            della pagina di modfica di un commento sia 200 nel caso in cui l'utente sia loggato e sta provando a modificare un commento scritto da lui e il thread è aperto"""

        self.client.login(username='testuser', password='password')

        # Creazione di un commento scritto da un altro utente
        self.comment2 = Comment.objects.create(text="Test2", thread=self.thread1, user=self.userStaff.profile)

        # Creazione di un commento scritto da me
        self.mycomment = Comment.objects.create(text="Test3", thread=self.thread1, user=self.user.profile)

        # # Prova a modificare il commento scritto da un altro utente
        self.errorComment = reverse('editComment', args=[self.category1.pk, self.thread1.pk, self.comment2.pk])
        response = self.client.get(self.errorComment)
        self.assertEqual(response.status_code, 403)

        # Prova a modificare il commento scritto da me
        self.EditCommentForum = reverse('editComment', args=[self.category1.pk, self.thread1.pk, self.mycomment.pk])
        response1 = self.client.get(self.EditCommentForum)
        self.assertEqual(response1.status_code, 200)

        # Prova a modificare il commento scritto da me in un thread chiuso
        # Chiudo il thread1
        self.thread1.is_active = False
        self.thread1.save()
        self.EditCommentForum = reverse('editComment', args=[self.category1.pk, self.thread1.pk, self.comment2.pk])
        response2 = self.client.get(self.EditCommentForum)
        self.assertEqual(response2.status_code, 403)
        self.thread1.is_active = True
        self.thread1.save()

    def testEditCommentForumNoLogin(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                                            della pagina di modfica di un commento sia 302 (redirect) nel caso in cui l'utente non sia loggato"""

        self.EditCommentForum = reverse('editComment', args=[self.category1.pk, self.thread1.pk, self.comment1.pk])
        response = self.client.get(self.EditCommentForum)
        self.assertEqual(response.status_code, 302)


    def testCreateCommentThreadForumLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        della pagina di inserimento di un commento all'interno di un thread sia 200 (buon fine), nel caso l'utente
        sia loggato."""

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.CreateCommentThreadForum)
        self.assertEqual(response.status_code, 200)
        # Si considera il che il thread non sia bloccato (campo is_active a True) per inserire un commento
        self.assertEqual(response.context['thread_lock'], True)

        # Se cerco di inserire un commento in un thread bloccato la risposta del server sarà 403 (permesso negato)
        # Creazione di un thread nella categoria Walk bloccato (is_active = False)
        self.thread_blocked = Thread.objects.create(title="ThreadWalk", text="Test", category=self.category1,
                                                    user=self.user.profile, is_active=False)
        self.CreateCommentThreadForum = reverse('createComment', args=['1', '2'])
        response = self.client.get(self.CreateCommentThreadForum)
        self.assertEqual(response.status_code, 403)
        self.thread_blocked.delete()


    def testCreateCommentThreadForumNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        della pagina di inserimento di un commento all'interno di un thread sia 302 (redirect), nel caso l'utente non
        sia loggato."""
        response = self.client.get(self.CreateCommentThreadForum)
        self.assertEqual(response.status_code, 302)


    def test_lockThreadLoggedStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                della pagina di blocco di un thread sia 302 (redirect), nel caso in cui l'utente loggato sia parte dello staff."""
        self.client.login(username='userStaff', password='password')
        response = self.client.get(self.lockThread)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Controllo che il thread venga bloccato
        # Creazione di un nuovo thread nella categoria Walk attivo (is_active = True)
        self.thread_blocked = Thread.objects.create(title="ThreadWalk", text="Test", category=self.category1,
                                                    user=self.user.profile)
        self.lockThread = reverse('lockThread', args=['1', self.thread_blocked.pk])
        response = self.client.get(self.lockThread)
        self.assertEqual(Thread.objects.filter(pk=self.thread_blocked.pk).last().is_active, False)
        self.thread_blocked.delete()


    def test_lockThreadLoggedNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        dell'url di blocco dell'inserimento dei commenti all'interno di un thread sia 302 (redirect), nel caso l'utente non
        sia parte dello staff."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.lockThread)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)


    def test_lockThreadNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        dell'url di blocco dell'inserimento dei commenti all'interno di un thread sia 302 (redirect), nel caso l'utente non
        sia loggato."""
        response = self.client.get(self.lockThread)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)


    def test_delete_threadLoggedStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        della pagina di eliminazione di un thread sia 302 (redirect), nel caso in cui l'utente loggato sia parte dello staff."""
        self.client.login(username='userStaff', password='password')
        response = self.client.get(self.delete_thread)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Controllo che il thread venga eliminato
        # Creazione di un nuovo thread nella categoria Walk
        self.thread_deleted = Thread.objects.create(title="ThreadWalk", text="Test", category=self.category1,
                                                    user=self.user.profile)
        self.thread_deleted = reverse('deleteThread', args=['1', self.thread_deleted.pk])
        response = self.client.get(self.thread_deleted)
        self.assertNotIn(self.thread_deleted, Thread.objects.all())


    def test_delete_threadLoggedNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                dell'url di eliminazione di un thread sia 302 (redirect), nel caso l'utente non
                sia parte dello staff."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.delete_thread)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)


    def test_delete_threadNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        dell'url di eliminazione di un thread sia 302 (redirect), nel caso l'utente non sia loggato."""
        response = self.client.get(self.delete_thread)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)


    def test_delete_commentLoggedStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        dell'url di eliminazione di un messaggio relativo ad un thread sia 302 (redirect), nel caso in cui l'utente loggato sia parte dello staff."""
        self.client.login(username='userStaff', password='password')
        response = self.client.get(self.delete_comment)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Controllo che il messaggio nel thread venga eliminato
        # Creazione di un nuovo messaggio nella categoria Walk, thread ThreadWalk
        self.comment_deleted = Comment.objects.create(text="Test", thread=self.thread1, user=self.user.profile)
        self.comment_deleted = reverse('deleteComment', args=[self.category1.pk, self.thread1.pk, self.comment_deleted.pk])
        response = self.client.get(self.delete_thread)
        self.assertNotIn(self.comment_deleted, Comment.objects.all())


    def test_delete_commentLoggedNoStaff(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
                dell'url di eliminazione di un messaggio relativo ad un thread sia 302 (redirect), nel caso l'utente non
                sia parte dello staff."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.delete_comment)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)


    def test_delete_commentNoLogged(self):
        """Verifica che la risposta del server al tentativo di una richiesta GET
        dell'url di eliminazione di un messaggio relativo ad un thread sia 302 (redirect), nel caso l'utente non sia loggato."""
        response = self.client.get(self.delete_comment)
        self.assertEqual(response.status_code, 302)
        self.assertEquals('/admin/login/' in response.url, True)
