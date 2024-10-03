from rest_framework import serializers
from django.contrib.auth.models import User
from reviews.models import Review, Game





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

    class Meta:
        model = Review
        fields = ['id', 'game', 'review_content', 'rating', 'user', 'created_date']
        read_only_fields = ['user', 'created_date']

    def validate(self, data):
        if data["rating"] < 1 or data["rating"] > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return data