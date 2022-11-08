from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `update`, and `list` actions.
    """
    pass