from rest_framework.permissions import IsAuthenticated

from .viewsets import ListRetrieveUpdateViewSet
from accounts.serializers import ProfileListSerializer
from accounts.models import Profile


class ProfileViewSet(ListRetrieveUpdateViewSet):
    '''A viewset to `list`, `update` and `retrieve` users profiles. '''

    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.role in ["ad", 'su']:
            return Profile.objects.all()

        return Profile.objects.filter(user=self.request.user)
    
    
    def get_serializer_class(self):
        # return appropriate serializer

        if self.action == "list":
            return ProfileListSerializer

