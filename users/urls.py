from django.urls import path
from users import views as users_views

urlpatterns = [
    path('profile/', users_views.UserProfileView.as_view(), name='user-profile'),
]