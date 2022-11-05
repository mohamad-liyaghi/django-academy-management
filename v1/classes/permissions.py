from rest_framework.permissions import BasePermission

class CoursePermission(BasePermission):

    def has_permission(self, request, view):
        # allow anyone to access lists
        if request.method == "GET":
            return True
        
        if request.method in ["POST", "PUT", "PATCH"]:
            if request.user.is_authenticated and request.user.role in ["su", "ad", 't']:
                return True

            return False
    