import os
import sys

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portaleTuristico.settings")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'portaleTuristico.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portaleTuristico.settings")

import django

django.setup()

from pathManagement.models import Path
import pandas as pd
import sklearn.metrics as sk


def featureStart(object):
    occurency = []
    for start, name in Path.locationChoices:
        if object.start == start:
            occurency.append(1)
        else:
            occurency.append(0)
    return occurency


def featureActivity(object):
    occurency = []
    for activity, name in Path.activityChoices:
        if activity in object.activity:
            occurency.append(1)
        else:
            occurency.append(0)
    return occurency


def featureAudience(object):
    occurency = []
    for audience, name in Path.audienceChoices:
        if audience in list(object.audience):
            occurency.append(1)
        else:
            occurency.append(0)
    return occurency


def featureDifficulty(object):
    occurency = []
    for difficulty, name in Path.difficultyChoices:
        if object.difficulty == difficulty:
            occurency.append(1)
        else:
            occurency.append(0)
    return occurency


def featureWalkTime(object):
    # Se il percorso è compreso tra 0 e 1h
    if object.walkTime <= 60:
        return [1, 0, 0, 0]
    elif 60 < object.walkTime <= 120:
        return [0, 1, 0, 0]
    elif 120 < object.walkTime <= 180:
        return [0, 0, 1, 0]
    else:
        # Se il percorso è maggiore di 3h
        return [0, 0, 0, 1]


def featureKilometers(object):
    # Se il percorso è compreso tra 0 e 6km
    if object.totalKilometers <= 6:
        return [1, 0, 0]
    elif 6 < object.totalKilometers <= 10:
        return [0, 1, 0]
    else:
        # Se il percorso è maggiore di 10 km
        return [0, 0, 1]


def listFeature(object):
    """Metodo che ritorna la lista delle feature presenti nell'object"""
    listRow = []

    # Aggiunta feature partenza
    listRow.extend(featureStart(object))

    # Aggiunta feature attivita
    listRow.extend(featureActivity(object))

    # Aggiunta feature utenza
    listRow.extend(featureAudience(object))

    # Aggiunta feature difficoltà
    listRow.extend(featureDifficulty(object))

    # Aggiunta feature walkTime
    listRow.extend(featureWalkTime(object))

    # Aggiunta feature lunghezza
    listRow.extend(featureKilometers(object))

    return listRow


def dictionaryPathFeature():
    """Metodo che crea un dizionario del tipo {'path_1': [0 0 1 0 ..]} a partire dai percorsi e feature presenti nel db"""

    dict_path = {}
    path = Path.objects.all()
    for p in path:
        dict_path[p.pk] = listFeature(p)

    return dict_path


class MatrixPathFeature:
    def __init__(self):
        # Creo la matrice
        self.matrix = pd.DataFrame(data=dictionaryPathFeature()).T

        # Calcolo la matrice delle similarità
        self.sim = sk.pairwise.cosine_similarity(self.matrix.values)

        # Calcolo del DataFrame della similarità
        self.sim_matrix = pd.DataFrame(self.sim, columns=self.matrix.index.values,
                                       index=list(self.matrix.index))

        self.sim_matrix.to_csv(os.path.join(os.getcwd(), 'matrix'))


if __name__ == '__main__':
    a = MatrixPathFeature()
    print(a.matrix)
    print(a.sim_matrix)
