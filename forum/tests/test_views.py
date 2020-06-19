from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

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