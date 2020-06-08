import os

from django.db import models
from multiselectfield import MultiSelectField


def user_directory_path(instance, filename):
    """Metodo che inserisce un file nella cartella relativa all'utente, il file sarà inserito nella cartella MEDIA_ROOT/user_<id>/<filename>
        :return user_<id>/<filename>"""
    return os.path.join('static', 'img', 'path_{0}', '{1}').format(instance.id, filename)


class Path(models.Model):
    """Classe che descrive la tabella dei percorsi, con campi: id,  """

    activityChoices = (
        ('relax', 'Relax'),
        ('didattica', 'Didattica'),
        ('esplorazione', 'Esplorazione'),
        ('escursionismo', 'Escursionismo'),
    )

    locationChoices = (
        ('bagnodiromagna', 'Bagno di Romagna'),
        ('sanpietroinbagno', 'San Pietro in Bagno'),
        ('acquapartita', 'Acquapartita'),
        ('laghi', 'Laghi'),
        ('alfero', 'Alfero'),
    )

    difficultyChoices = (
        ('facile', 'Facile'),
        ('medio', 'Medio'),
        ('difficile', 'Difficile'),
    )

    contextChoices = (
        ('collinare', 'Collinare'),
        ('urbano', 'Urbano'),
        ('fluviale', 'Fluviale'),
        ('boschivo', 'Boschivo'),
        ('laghi', 'Laghi'),
    )

    transportChoices = (
        ('automobile', 'Automobile'),
        ('bicidacittà', 'Bici da città'),
        ('piedi', 'Piedi'),
        ('mountainbike', 'Mountain bike'),
    )

    audienceChoices = (
        ('famiglia', 'Famiglia'),
        ('gruppi', 'Gruppi'),
        ('coppie', 'Coppie'),
        ('mobilitàridotta', 'Mobilità ridotta'),
        ('escursionisti', 'Escursionisti'),
        ('sportivi', 'Sportivi'),
    )

    id = models.IntegerField(primary_key=True)
    activity = models.CharField(max_length=30, choices=activityChoices)
    start = models.CharField(max_length=30, choices=locationChoices)
    end = models.CharField(max_length=30, choices=locationChoices)
    gradient = models.IntegerField()
    walkTime = models.IntegerField()
    bikeTime = models.IntegerField(blank=True, default=0)
    carriageablePath = models.FloatField(blank=True, default=0)
    nonCarriageablePath = models.FloatField(blank=True, default=0)
    difficulty = MultiSelectField(choices=difficultyChoices)
    difficultyImage = models.ImageField(blank=False, upload_to=user_directory_path)
    context = MultiSelectField(choices=contextChoices)
    contextImage = models.ImageField(blank=False, upload_to=user_directory_path)
    transport = MultiSelectField(choices=transportChoices)
    transportImage = models.ImageField(blank=False, upload_to=user_directory_path)
    audience = MultiSelectField(choices=audienceChoices)
    audienceImage = models.ImageField(blank=False, upload_to=user_directory_path)
    path = models.ImageField(blank=False, upload_to=user_directory_path)
