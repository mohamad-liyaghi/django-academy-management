from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .viewsets import CreateListRetrieveUpdateViewSet, ListRetrieveUpdateViewSet
from accounts.serializers import CreateRequestSerializer, ProfileDetailSerializer, ProfileListSerializer, RequestDetailSerializer, RequestListSerializer, UpdateRequestSerializer
from accounts.models import Profile, Request


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
        '''Update a profile. Only profile owner can update.'''

        if self.request.user == self.get_object().user:
            return super().update(request, *args, **kwargs)

        return Response("You dont have permission to update this profile.", status=status.HTTP_403_FORBIDDEN)
            


class RequestViewSet(CreateListRetrieveUpdateViewSet):
    '''A viewset to `create`, `list`, `update` and `retrieve` users requests. '''

    queryset = Request.objects.all()
    permission_classes = [IsAuthenticated,]


    def get_serializer_context(self):
        return {"user" : self.request.user}


    def get_serializer_class(self):
        if self.action == "list":
            return RequestListSerializer

        elif self.action == "create":
            return CreateRequestSerializer
        
        elif self.action == "retrieve":
            return RequestDetailSerializer
        
        elif self.action in ["update", 'partial_update']:
            return UpdateRequestSerializer


    def get_queryset(self):
        if self.request.user.role in ["ad", "su"]:
            return Request.objects.all().order_by("date")

        return Request.objects.filter(user=self.request.user).order_by("date")


    def get_object(self):
        if self.request.user.role in ["ad", "su"]:
            return super().get_object()

        return get_object_or_404(Request, id=self.kwargs["pk"], 
                    user= self.request.user)


@api_view(["GET"])
def get_money(request):
    '''Exchange money endpoint. you should implement payment methods here'''

    if request.user.is_authenticated:

        request.user.balance = request.user.balance + 20
        request.user.save() 
        return Response(f"20 coins added to your account balance, your balance: {request.user.balance}", 
                    status=status.HTTP_200_OK)

    else:
        return Response("User is not authenticated.", status=status.HTTP_401_UNAUTHORIZED)

