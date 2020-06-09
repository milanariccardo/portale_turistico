import django_filters
from .models import Path


class PathFilter(django_filters.FilterSet):

    end_time = django_filters.NumberFilter(field_name='walkTime',method= 'hoursToMinutes',lookup_expr='lte')

    class Meta:
        model = Path
        fields = ['activity', 'start', 'walkTime']

    def hoursToMinutes(self, queryset, name, value):
        value = int(value)*60
        return queryset.filter(walkTime__lte = value)