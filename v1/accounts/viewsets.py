from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `update`, and `list` actions.
    """
    pass


class CreateListRetrieveUpdateViewSet(ListRetrieveUpdateViewSet,
                                    mixins.CreateModelMixin):
    
    """
        A viewset that provides `create`, `retrieve`, `update`, and `list` actions.
    """
    pass