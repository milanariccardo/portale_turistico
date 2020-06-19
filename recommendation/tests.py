import numpy
from django.test import TestCase
import os
from pathManagement.models import Path
from recommendation.recommendation import featureStart, featureActivity, featureAudience, featureDifficulty, \
    featureWalkTime, featureKilometers, listFeature, dictionaryPathFeature, MatrixPathFeature


class TestfunctionRecommendation(TestCase):

    def setUp(self):
        """ Metodo per impostare l'ambiente in cui si svolge il test: viene creato uno percorso """

        self.url_image = os.path.join(os.getcwd(), 'static', 'img', 'favicon.ico')
        self.path = Path.objects.create(id=1, activity=['relax'], start="laghi", end="alfero", gradient=10,
                                        walkTime=30, bikeTime=20, carriageablePath=3.4, nonCarriageablePath=2,
                                        difficulty="facile", context=['collinari'], transport=["piedi", ],
                                        audience=['gruppi'], difficultyImage=self.url_image,
                                        contextImage=self.url_image, transportImage=self.url_image,
                                        audienceImage=self.url_image,
                                        path=self.url_image, cover=self.url_image)

    def testfeatureStart(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureStart(self.path), [0, 0, 0, 1, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureStart, 'string')
        self.assertRaises(TypeError, featureStart, ('string1', 'string2', 2, 3.2))

    def testfeatureActivity(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureActivity(self.path), [1, 0, 0, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureActivity, 'string')
        self.assertRaises(TypeError, featureActivity, ('string1', 'string2', 2, 3.2))

    def testfeatureAudience(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureAudience(self.path), [0, 1, 0, 0, 0, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureAudience, 'string')
        self.assertRaises(TypeError, featureAudience, ('string1', 'string2', 2, 3.2))

    def testfeatureDifficulty(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureDifficulty(self.path), [1, 0, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureDifficulty, 'string')
        self.assertRaises(TypeError, featureDifficulty, ('string1', 'string2', 2, 3.2))

    def testfeatureWalkTime(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureWalkTime(self.path), [1, 0, 0, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureWalkTime, 'string')
        self.assertRaises(TypeError, featureWalkTime, ('string1', 'string2', 2, 3.2))

    def testfeatureKilometers(self):
        # Testing del metodo nel caso di input accettabile
        self.assertEqual(featureKilometers(self.path), [1, 0, 0])

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, featureKilometers, 'string')
        self.assertRaises(TypeError, featureKilometers, ('string1', 'string2', 2, 3.2))

    def testlistFeature(self):
        # Testing del metodo nel caso di input accettabile
        correct_list = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        self.assertEqual(listFeature(self.path), correct_list)

        # Testing del metodo nel caso di input non di tipo 'Path': stringhe, tuple
        self.assertRaises(TypeError, listFeature, 'string')
        self.assertRaises(TypeError, listFeature, ('string1', 'string2', 2, 3.2))

    def testdictionaryPathFeature(self):
        # Testing del metodo nel caso di input accettabile
        correct_list = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        self.assertEqual(dictionaryPathFeature(), {self.path.pk: correct_list})

        # Testing del metodo nel caso in cui non esiste alcun percorso nel database
        # Elimazione del percoso
        self.path.delete()
        self.assertEqual(dictionaryPathFeature(), {})


class TestMatrixPathFeature(TestCase):

    def setUp(self):
        """ Metodo per impostare l'ambiente in cui si svolge il test: viene creato uno percorso """

        self.url_image = os.path.join(os.getcwd(), 'static', 'img', 'favicon.ico')

        # Inserimento di 3 percorsi nel database
        self.path1 = Path.objects.create(id=1,
                                         activity=['relax'],
                                         start="laghi",
                                         end="alfero",
                                         gradient=10,
                                         walkTime=30,
                                         bikeTime=20,
                                         carriageablePath=3.4,
                                         nonCarriageablePath=2,
                                         difficulty="facile",
                                         context=['collinari'],
                                         transport=["piedi", ],
                                         audience=['gruppi'],
                                         difficultyImage=self.url_image,
                                         contextImage=self.url_image,
                                         transportImage=self.url_image,
                                         audienceImage=self.url_image,
                                         path=self.url_image,
                                         cover=self.url_image)


        self.path2 = Path.objects.create(id=2,
                                         activity=['relax', 'didattica'],
                                         start="alfero",
                                         end="bagnodiromagna",
                                         gradient=3,
                                         walkTime=100,
                                         bikeTime=30,
                                         carriageablePath=5,
                                         nonCarriageablePath=0,
                                         difficulty="medio",
                                         context=['collinari'],
                                         transport=["piedi", 'automobile'],
                                         audience=['coppie'],
                                         difficultyImage=self.url_image,
                                         contextImage=self.url_image,
                                         transportImage=self.url_image,
                                         audienceImage=self.url_image,
                                         path=self.url_image,
                                         cover=self.url_image)

        self.path3 = Path.objects.create(id=3,
                                         activity=['escursionismo', 'esplorazione'],
                                         start="bagnodiromagna",
                                         end="acquapartita",
                                         gradient=0,
                                         walkTime=40,
                                         bikeTime=10,
                                         carriageablePath=3,
                                         nonCarriageablePath=40,
                                         difficulty="difficile",
                                         context=['collinari'],
                                         transport=['bicidacittà', 'piedi'],
                                         audience=['sportivi'],
                                         difficultyImage=self.url_image,
                                         contextImage=self.url_image,
                                         transportImage=self.url_image,
                                         audienceImage=self.url_image,
                                         path=self.url_image,
                                         cover=self.url_image)


    def testMatrixPathFeatureInstance(self):
        # Test che verifica la consistenza architetturale
        self.assertTrue(isinstance(MatrixPathFeature(), MatrixPathFeature))

    def testValidMatrixPathFeature(self):
        # Test che verifica la corretta composizione della matrice matrix della classe MatrixPathFeature
        correct_list_path1 = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        correct_list_path2 = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        correct_list_path3 = [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        correct_sim_matrix = [[1, 0.3086067, 0.15430335],
                              [0.3086067, 1, 0],
                              [0.15430335, 0, 1]
                              ]
        self.assertTrue(numpy.array_equal(numpy.array(correct_sim_matrix).all(), MatrixPathFeature().sim.all()))


        # Se non ci sono percorsi nel database
        # Elimina i percorsi dal database:
        self.path1.delete()
        self.path2.delete()
        self.path3.delete()
        self.assertRaises(ValueError, MatrixPathFeature, )


