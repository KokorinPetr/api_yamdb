from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics, mixins
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleListRetriveserializer,
)
from titles.models import Category, Genre, Title


# class ListCreateDeleteViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     pass

# class CategoryViewSet(ListCreateDeleteViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     pagination_class = LimitOffsetPagination

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDestroyView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDestroyView(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return TitleListRetriveserializer
        return TitleSerializer
