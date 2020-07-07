import os

from django.contrib.auth.models import User

from userManagement.models import Profile
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator


def user_directory_path(instance, filename):
    """Metodo che che crea la cartella e inserisce le immagini nella cartella relativa al percorso, il file sarà inserito nella cartella MEDIA_ROOT/img/static/path_<id>/<filename>
        :return path_<id>/<filename>"""
    return os.path.join('static', 'img', 'path_{0}', '{1}').format(instance.id, filename)


def user_review_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.review.user.id, filename)


class Path(models.Model):
    """Classe che descrive la tabella dei percorsi"""

    activityChoices = (
        ('relax', 'Relax'),
        ('didattica', 'Didattica'),
        ('esplorazione', 'Esplorazione'),
        ('escursionismo', 'Escursionismo'),
    )

    locationChoices = (
        ('bagnodiromagna', 'Bagno di Romagna'),
        ('sanpietroinbagno', 'San Piero in Bagno'),
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

    id = models.PositiveIntegerField(primary_key=True)
    activity = models.CharField(max_length=30, choices=activityChoices)
    start = models.CharField(max_length=30, choices=locationChoices)
    end = models.CharField(max_length=30, choices=locationChoices)
    gradient = models.IntegerField()
    walkTime = models.PositiveIntegerField()
    bikeTime = models.PositiveIntegerField(blank=True, default=0)
    carriageablePath = models.FloatField(blank=True, default=0, validators=[MinValueValidator(0)])
    nonCarriageablePath = models.FloatField(blank=True, default=0, validators=[MinValueValidator(0)])
    totalKilometers = models.FloatField(editable=False, blank=True, default='0')
    difficulty = models.CharField(max_length=30, choices=difficultyChoices)
    difficultyImage = models.ImageField(blank=False, upload_to=user_directory_path)
    context = MultiSelectField(choices=contextChoices)
    contextImage = models.ImageField(blank=False, upload_to=user_directory_path)
    transport = MultiSelectField(choices=transportChoices)
    transportImage = models.ImageField(blank=False, upload_to=user_directory_path)
    audience = MultiSelectField(choices=audienceChoices)
    audienceImage = models.ImageField(blank=False, upload_to=user_directory_path)
    path = models.ImageField(blank=False, upload_to=user_directory_path)
    cover = models.ImageField(blank=False, upload_to=user_directory_path)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.totalKilometers = self.carriageablePath + self.nonCarriageablePath
        super(Path, self).save(*args, **kwargs)


class Review(models.Model):
    class Meta:
        unique_together = (('path', 'user'),)

    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    valuation = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(blank=False, max_length=255)
    comment = models.TextField(blank=False, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_profile(self):
        return Profile.objects.filter(user=self.user.id).get()

    def get_create_date(self):
        return self.created_at.strftime("%d/%m/%Y")


class ListPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to=user_review_directory_path)
