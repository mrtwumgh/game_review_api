from users.models import Profile
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from users.serializers import ProfileSerializer
from rest_framework.response import Response


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
