import django_filters
from django.forms import DateTimeInput
from django_filters import ChoiceFilter
from .models import Path, Review

hour_choiches = (
    ('1', '1 ora'),
    ('2', '2 ore'),
    ('3', '3 ore'),
    ('4', '4 ore'),
    ('5', '5 ore'),
    ('25', 'Più di 5 ore'),
)

order_choiches = (
    ('pc', 'Lunghezza percorso crescente'),
    ('pd', 'Lunghezza percorso decrescente'),
    ('tpc', 'Tempo a piedi crescente'),
    ('tpd', 'Tempo a piedi decrescente'),
    ('r', 'Valutazione crescente'),
    ('p', 'Valutazione decrescente'),

)


def order_valuations(queryset, best):
    """Funzione che permette di recuperare il queryset ordinato secondo la valutazione del percorso
    :param queryset: queryset su cui ordinare
    :param best: True per una valutazione crescente, False per una valutazione decrescente
    :return queryset ordinato per valutazione"""

    review = {}
    # Creazione di un dizionario {path.pk:valuation}
    for path in queryset:
        review[path.pk] = 0
        val = Review.objects.filter(path=path).values('valuation')
        iteration = val.count()

        for i in val:
            review[path.pk] = review[path.pk] + i['valuation'] / iteration

    # Creazione lista contentente le chiavi dei path ordinati, se True ordinamento per valutazioni crescenti se False ordinamento per valutazioni decrescenti
    if best:
        list_pk = sorted(review, key=review.get)[::-1]
    else:
        list_pk = sorted(review, key=review.get)

    # Associazione di ogni elemento della lista list_pk alla posizione nel queryset
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(list_pk)])
    ordering = 'CASE %s END' % clauses

    # Creazione queryset
    queryset = Path.objects.filter(pk__in=list_pk).extra(
        select={'ordering': ordering}, order_by=('ordering',))
    return queryset


class PathFilter(django_filters.FilterSet):
    end_time = django_filters.ChoiceFilter(choices=hour_choiches, field_name='walkTime', method='hoursToMinutes',
                                           lookup_expr='lte', label='Quanto tempo vuoi camminare?')
    km_min = django_filters.NumberFilter(field_name='totalKilometers', lookup_expr='gte',
                                         label="Numero di kilometri minimo")
    km_max = django_filters.NumberFilter(field_name='totalKilometers', lookup_expr='lte',
                                         label="Numero di kilometri massimo")
    ordering = django_filters.ChoiceFilter(choices=order_choiches, label='Ordina risultati per', method='filter_by')

    class Meta:
        model = Path
        fields = ['activity', 'start']

    def __init__(self, *args, **kwargs):
        super(PathFilter, self).__init__(*args, **kwargs)
        self.filters['activity'].label = "Che attività vuoi svolgere?"
        self.filters['start'].label = "Da che punto hai intenzione di partire?"

    def hoursToMinutes(self, queryset, name, value):
        value = int(value) * 60
        return queryset.filter(walkTime__lte=value)

    def filter_by(self, queryset, name, value):
        if value == 'pc':
            return queryset.order_by('totalKilometers')
        elif value == 'pd':
            return queryset.order_by('-totalKilometers')
        elif value == 'tpc':
            return queryset.order_by('walkTime')
        elif value == 'tpd':
            return queryset.order_by('-walkTime')
        elif value == 'r':
            return order_valuations(queryset, True)
        elif value == 'p':
            return order_valuations(queryset, False)
