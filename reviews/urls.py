from django.urls import path
from reviews import views as review_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', review_views.UserRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('hello/', review_views.HelloWorldView.as_view(), name='hello-world'),
]