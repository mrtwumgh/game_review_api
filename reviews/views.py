from reviews.serializers import (
    UserRegistrationSerializer,
    ReviewSerializer,
    GameSerializer,
)
from rest_framework import generics, permissions, filters, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from reviews.models import Review, Game, ReviewLike
from users.models import Profile
from reviews.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': response.data,
            'token': token.key
        })



class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['rating', 'game__title']
    search_fields = ['review_content', 'game_title']
    ordering_fields = ['rating', 'created_date']
    ordering = ['-created_date']

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

# Action Views
class LikeReview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
        if not created:
            return Response({"detail": "You already liked this review."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Review Liked"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        like = ReviewLike.objects.filter(user=request.user, review=review)
        if like.exists():
            like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You have not liked this review"}, status=status.HTTP_400_BAD_REQUEST)
    

class MostLikedReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        game_title = self.request.query_params.get('game_title', None)
        if game_title:
            return Review.objects.filter(game__title=game_title).annotate(like_count=Count('likes')).order_by('-like_count')
        else:
            return Review.objects.annotate(like_count=Count('likes')).order_by('-like_count')


# Game Title Views
class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]

class GameDetailView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]