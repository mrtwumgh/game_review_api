from rest_framework import serializers
from django.contrib.auth.models import User
from reviews.models import Review, Game, ReviewLike, Comment





class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title']



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_date = serializers.ReadOnlyField()
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='title')
    like_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'game', 'review_content', 'rating', 'user', 'created_date', 'like_count']
        read_only_fields = ['user', 'created_date']

    def validate(self, data):
        if data["rating"] < 1 or data["rating"] > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return data
    

class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_date = serializers.ReadOnlyField()
    updated_date = serializers.ReadOnlyField()
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'content', 'created_date', 'updated_date']
        read_only_fields = ['user', 'review', 'created_date', 'updated_date']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty")
        return value