from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsProvider
from .serializers import BaseServiceSerializer, ProviderServiceSerializer
from services.models import BaseService, ProviderService
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Base Service'])
class BaseServiceViewSet(viewsets.ModelViewSet):

    queryset = BaseService.objects.all()
    serializer_class = BaseServiceSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=['Provider Service'])
class ProviderSerivceViewSet(viewsets.ModelViewSet):

    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        return ProviderService.objects.filter(provider = self.request.user)
    
    def perform_create(self, serializer):
        
        serializer.save(provider = self.request.user)
    
    def perform_update(self, serializer):
        
        serializer.save(provider = self.request.user)
    
    def perform_destroy(self, instance):
        
        instance.delete()

@extend_schema(tags=['Provider Service for customers'])
class ProviderServiceListForCustomerView(generics.ListAPIView):

    serializer_class = ProviderServiceSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        
        provider_id = self.kwargs['provider_id']

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            provider = User.objects.get(id = provider_id, role = 'p')
        
        except User.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("provider not found.")
        
        return ProviderService.objects.filter(provider=provider)