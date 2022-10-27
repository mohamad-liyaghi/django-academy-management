from .viewsets import ListRetrieveUpdateViewSet
from accounts.models import Profile


class ProfileViewSet(ListRetrieveUpdateViewSet):
    '''A viewset to `list`, `update` and `retrieve` users profiles. '''

    queryset = Profile.objects.all()

