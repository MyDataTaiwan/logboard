import django_filters

from apps.records.models import Record


class RecordFilter(django_filters.FilterSet):
    uid = django_filters.CharFilter(field_name='owner__id')
    template = django_filters.CharFilter(field_name='template_name')
    start_date = django_filters.NumberFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.NumberFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Record
        fields = ('uid', 'template', 'start_date', 'end_date')
