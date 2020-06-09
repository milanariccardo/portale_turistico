import django_filters
from django.forms import DateTimeInput
from django_filters import ChoiceFilter
from .models import Path

hour_choiches = (
    ('1', '1h'),
    ('2', '2h'),
    ('3', '3h'),
    ('4', '4h'),
    ('5', '5h'),
    ('25', 'Più di 5 ore'),
)

class PathFilter(django_filters.FilterSet):

    end_time = django_filters.ChoiceFilter(choices=hour_choiches, field_name='walkTime', method= 'hoursToMinutes', lookup_expr='lte', label='Quanto tempo vuoi dedicare?')
    km_min = django_filters.NumberFilter(field_name='totalKilometers', lookup_expr='gte', label="Numero di kilometri minimo")
    km_max = django_filters.NumberFilter(field_name='totalKilometers', lookup_expr='lte', label="Numero di kilometri massimo")

    class Meta:
        model = Path
        fields = ['activity', 'start']

    def __init__(self, *args, **kwargs):
        super(PathFilter, self).__init__(*args, **kwargs)
        self.filters['activity'].label = "Che attività vuoi svolgere?"
        self.filters['start'].label = "Da che punto hai intenzione di partire?"

    def hoursToMinutes(self, queryset, name, value):
        value = int(value)*60
        return queryset.filter(walkTime__lte = value)