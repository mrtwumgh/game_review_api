from django.urls import path
from reviews import views as review_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', review_views.UserRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('reviews/', review_views.ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', review_views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', review_views.ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:pk>/update/', review_views.ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete', review_views.ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/<int:pk>/like/', review_views.LikeReview.as_view(), name='like-review'),
    path('reviews/most-liked/', review_views.MostLikedReviews.as_view(), name='most-liked'),
    # Game list urls
    path('games/', review_views.GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', review_views.GameDetailView.as_view(), name='game-detail')
]