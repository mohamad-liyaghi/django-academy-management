from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .viewsets import ListRetrieveUpdateViewSet
from accounts.serializers import ProfileDetailSerializer, ProfileListSerializer
from accounts.models import Profile


class ProfileViewSet(ListRetrieveUpdateViewSet):
    '''A viewset to `list`, `update` and `retrieve` users profiles. '''

    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.role in ["ad", 'su']:
            return Profile.objects.all()

        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        if self.request.user.role in ["ad", 'su', 't']:
            return get_object_or_404(Profile, id=self.kwargs["pk"])

        return get_object_or_404(Profile, id=self.kwargs["pk"], user=self.request.user)
    
    
    def get_serializer_class(self):
        # return appropriate serializer

        if self.action == "list":
            return ProfileListSerializer

        elif self.action in ["retrieve", "update", "partial_update"]:
            return ProfileDetailSerializer

