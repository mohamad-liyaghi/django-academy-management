from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `update`, and `list` actions.
    """
    def list(self, request, *args, **kwargs):
        '''Superuser can see list of all purchases but normal users can see only their transactions.'''
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        '''A payment records detail page'''
        return super().retrieve(request, *args, **kwargs)