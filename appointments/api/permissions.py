from rest_framework.permissions import BasePermission



class IsCustomerOnly(BasePermission):

    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.role =='c'
    
    def has_object_permission(self, request, view, obj):
        
        return obj.customer == request.user
        
        
    
