from rest_framework.permissions import BasePermission


class AnonPermissionOnly(BasePermission):
    """
    A custom permission for non-authenticated users only, 
    that they are the only ones who can visit the authentication urls, registeration and login.
    """
    
    message = "You are already authenticated. Please log out and try again!"

    def has_permission(self, request, view):
        return not request.user.is_authenticated