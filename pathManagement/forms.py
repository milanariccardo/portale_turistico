from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from pathManagement.models import Path


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
