import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    min_time = django_filters.TimeFilter(field_name="init_time", lookup_expr="gte")
    max_time = django_filters.TimeFilter(field_name="init_time", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["description", "status", "min_time", "max_time"]
