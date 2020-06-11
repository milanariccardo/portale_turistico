from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from pathManagement.models import Path, Review


class InsertPathForm(ModelForm):
    class Meta:
        model = Path
        fields = '__all__'
        labels = {
            'id': _('Id percorso'),
            'activity': _('Attività'),
            'start': _('Luogo di partenza'),
            'end': _('Luogo di arrivo'),
            'gradient': _('Pendenza'),
            'walkTime': _('Tempo a piedi (in minuti)'),
            'bikeTime': _('Tempo in bici (in minuti)'),
            'carriageablePath': _('Strada carrabile (in km)'),
            'nonCarriageablePath': _('Strada sterrata (in km)'),
            'difficulty': _('Difficoltà'),
            'difficultyImage': _('Immagine relativa alla difficoltà'),
            'context': _('Contesto paesaggistico'),
            'contextImage': _('Immagine relativa al contesto paesaggistico'),
            'transport': _('Mezzi di trasporto utilizzabili'),
            'transportImage': _('Immagine relativa ai mezzi di trasporto utilizzabili'),
            'audience': _('Utenza'),
            'audienceImage': _("Immagine relativa all'utenza"),
            'path': _("Mappa del percorso"),
            'cover': _("Foto di copertina"),
        }


class EditPathForm(ModelForm):
    class Meta:
        model = Path
        fields = '__all__'
        exclude = ['id']
        labels = {
            'activity': _('Attività'),
            'start': _('Luogo di partenza'),
            'end': _('Luogo di arrivo'),
            'gradient': _('Pendenza'),
            'walkTime': _('Tempo a piedi (in minuti)'),
            'bikeTime': _('Tempo in bici (in minuti)'),
            'carriageablePath': _('Strada carrabile (in km)'),
            'nonCarriageablePath': _('Strada sterrata (in km)'),
            'difficulty': _('Difficoltà'),
            'difficultyImage': _('Immagine relativa alla difficoltà'),
            'context': _('Contesto paesaggistico'),
            'contextImage': _('Immagine relativa al contesto paesaggistico'),
            'transport': _('Mezzi di trasporto utilizzabili'),
            'transportImage': _('Immagine relativa ai mezzi di trasporto utilizzabili'),
            'audience': _('Utenza'),
            'audienceImage': _("Immagine relativa all'utenza"),
            'path': _("Mappa del percorso"),
            'cover': _("Foto di copertina"),
        }


class InsertPathReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'valuation']
        labels = {
            'comment': _('Commento'),
        }

    def __init__(self, *args, **kwargs):
        super(InsertPathReviewForm, self).__init__(*args, **kwargs)
        print(kwargs)

    def save(self, commit=True):
        instance = super(InsertPathReviewForm, self).save(commit=False)
        instance.valuation = self.cleaned_data['valuation']
        instance.comment = self.cleaned_data['comment']
        print()

        # if commit:
        #     instance.save()
        # return instance

        pass

    # def save(self, commit=True):
    #     instance = self.save(commit=False)
    #
    #     path = Path.objects.filter(id = self.kwargs[1])
    #     user = User.objects.filter(pk = self.kwargs[0])
    #     profile = Profile.objects.filter(user = user)
    #     instance.user = profile
    #     instance.path = path
    #     instance.save()
    #     print(self.request.user())
