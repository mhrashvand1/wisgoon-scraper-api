from django_filters import rest_framework as filters
from core.models import Post


class PostFilter(filters.FilterSet):
    source_created__lt = filters.DateTimeFilter(field_name='source_created', lookup_expr='lt')
    source_created__gt = filters.DateTimeFilter(field_name='source_created', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ('source_created',)