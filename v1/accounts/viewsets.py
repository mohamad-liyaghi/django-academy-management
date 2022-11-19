from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `update`, and `list` actions.
    """
    def list(self, request, *args, **kwargs):
        '''
            Superusers can see all user profiles but normal users can see only their profiles.
        '''
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        '''
            Profile detail page. Admins can see all profiles but normal users can only see their profiles.
        '''
        return super().retrieve(request, *args, **kwargs)
    
    


class CreateListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    
    """
        A viewset that provides `create`, `retrieve`, `update`, and `list` actions.
    """
    def create(self, request, *args, **kwargs):
        """Create a request for being admin or teacher."""
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        '''Update a request status or information.'''
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        '''Superuser can see all requests in db but normal users can only see their requests.'''
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        '''Request detail page'''
        return super().retrieve(request, *args, **kwargs)
