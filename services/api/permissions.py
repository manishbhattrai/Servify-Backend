from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated and request.user.role == 'p':
            
            return True
        
        return False

    def has_object_permission(self, request, view, obj):


       if request.user == obj.provider or request.user.is_staff:
           
           return True
       
       return False