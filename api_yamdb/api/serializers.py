from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        review = Review.objects.filter(title=obj.id)
        if review.exists() == True:
            return round(review.aggregate(Avg('score'))['score__avg'], 1)
        return 0


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!',
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('__all__')
        model = Comment
