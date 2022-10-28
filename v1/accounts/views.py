from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status

from django.shortcuts import get_object_or_404

from .viewsets import ListRetrieveUpdateViewSet
from accounts.serializers import ProfileDetailSerializer, ProfileListSerializer
from accounts.models import Profile


class ProfileViewSet(ListRetrieveUpdateViewSet):
    '''A viewset to `list`, `update` and `retrieve` users profiles. '''

    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated,]
    search_fields = ['user__email', "passport_number"]
    filter_backends = (filters.SearchFilter,)

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


    def update(self, request, *args, **kwargs):
        '''Dont let others to update a users profile'''

        if self.request.user == self.get_object().user:
            return super().update(request, *args, **kwargs)

        return Response("You dont have permission to update this profile.", status=status.HTTP_403_FORBIDDEN)
            

