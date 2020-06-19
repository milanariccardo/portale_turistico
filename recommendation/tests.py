from django.test import TestCase

from pathManagement.models import Path


class TestRecommendation(TestCase):

    def setUp(self):
        """ Metodo per impostare l'ambiente in cui si svolge il test: viene creato uno percorso """
        self.path = Path.objects.create(id=1, activity=('Relax',), start="Laghi", end="Alfero", gradient=10,
                                        walkTime=30, bikeTime=20, carriageablePath=3.4, nonCarriageablePath=2,
                                        difficulty="Facile", context=('Collinari',), transport=("Piedi",))

    def testfeatureStart(self):
