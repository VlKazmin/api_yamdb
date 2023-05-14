from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтры для модели Title.

    Позволяют осуществлять фильтрацию по различным полям модели Title.
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название произведения (поиск по части названия)'
    )
    year = filters.NumberFilter(
        field_name='year',
        label='Год выпуска'
    )
    category = filters.CharFilter(
        field_name="category__slug",
        label='Категория (поиск по слагу)'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        label='Жанр (поиск по слагу)'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
