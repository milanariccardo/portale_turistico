from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from pathManagement.models import Path, Review, ListPhoto
from userManagement.models import Profile

label_dict = {
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


class InsertPathForm(ModelForm):
    class Meta:
        model = Path
        fields = '__all__'
        insert_label_dict = label_dict
        insert_label_dict['id'] = _("Id")
        labels = insert_label_dict


class EditPathForm(ModelForm):
    class Meta:
        model = Path
        fields = '__all__'
        exclude = ['id']
        labels = label_dict


class InsertPathReviewForm(ModelForm):
    image = forms.ImageField(required=False, label='Inserisci immagine',widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Review
        fields = ['title', 'comment', 'valuation', ]
        labels = {
            'comment': _('Commento'),
            'valuation': _('Valutazione da 1 a 5'),
            'title': _('Inserisci un titolo'),

        }

    pk_user = None
    pk_path = None

    def __init__(self, *args, **kwargs):
        super(InsertPathReviewForm, self).__init__(*args, **kwargs)
        self.pk_user = kwargs.get('initial').get('pk1')
        self.pk_path = kwargs.get('initial').get('pk2')

    def save(self, commit=True):
        instance = super(InsertPathReviewForm, self).save(commit=False)
        instance.valuation = self.cleaned_data['valuation']
        instance.comment = self.cleaned_data['comment']

        path = Path.objects.filter(id=self.pk_path).last()
        user = User.objects.filter(pk=self.pk_user).last()
        profile = Profile.objects.filter(user=user).last()
        instance.path = path
        instance.user = profile

        if commit:
            instance.save()
        return instance


class EditPathReviewForm(ModelForm):
    image = forms.ImageField(required=False, label='Inserisci immagine', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Review
        fields = ['title', 'valuation', 'comment']
        labels = {
            'comment': _('Commento'),
            'valuation': _('Valutazione'),
            'title': _('Inserisci un titolo'),
        }