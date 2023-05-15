from rest_framework import serializers

from reviews.models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('__all__')
        model = Comment
