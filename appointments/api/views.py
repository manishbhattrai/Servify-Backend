from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CreateAppointmentSerializer, CustomerGetAppointmentsSerializer, ProviderAppointmentSerializer
from appointments.models import Appointments
from .permissions import IsCustomerOnly
from drf_spectacular.utils import extend_schema
from users.models import ProviderProfile, CustomerProfile



@extend_schema(tags=['Customer Create appointments'])
class CreateAppointmentView(generics.CreateAPIView):

    queryset = Appointments.objects.all()
    serializer_class = CreateAppointmentSerializer
    permission_classes = [IsCustomerOnly]


    def perform_create(self, serializer):

        customer_profile = CustomerProfile.objects.get(user=self.request.user)
        
        return serializer.save(customer = customer_profile)

@extend_schema(tags=['Customer get and update appointments'])
class CustomerGetUpdateappointmentView(APIView):

    serializer_class = CustomerGetAppointmentsSerializer
    permission_classes = [IsCustomerOnly]

    def get(self,request):

        user = self.request.user

        if user.role != 'c':
            return Response({"message":"Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer_profile = CustomerProfile.objects.get(user=user)
        
        except CustomerProfile.DoesNotExist:
            return Response({'message':"Profile doesnot exists."},status=status.HTTP_404_NOT_FOUND)
        
        
        appointments = Appointments.objects.filter(customer=customer_profile)

        serializer = self.serializer_class(appointments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request,*agrs, **kwargs):
        
        id = self.kwargs.get('id')

        appointments = get_object_or_404(Appointments, id=id)
                         
        appointments.status = 'cancelled'
        appointments.save()

        return Response({"message":"Appointment cancelled sucessfully."},status=status.HTTP_200_OK)

from services.api.permissions import IsProvider
@extend_schema(tags=['Provider get and update appointments'])
class ProviderAppointmentView(APIView):

    serializer_class = ProviderAppointmentSerializer

    
    permission_classes = [IsProvider]


    def get(self,request,*args, **kwargs):

        user = self.request.user

        if user.role != 'p':
            return Response({"message":"unauthorized"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            provider_profile = ProviderProfile.objects.get(user=user)
        
        except ProviderProfile.DoesNotExist:
            return Response({"message":"provider profile doesnot exists."},status=status.HTTP_400_BAD_REQUEST)
        
        appointments = Appointments.objects.filter(provider=provider_profile)

        if not appointments.exists():
            return Response({"message":"Appointment doesnot exists."},status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProviderAppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request ,*args, **kwargs):

        id = self.kwargs.get('id')

        appointments = get_object_or_404(Appointments, id=id)

        new_status = request.data.get('status')

        if not new_status:
            return Response({"message":"status is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if appointments.status != 'pending':
            return Response({"message":"only pending message can be approved or reject."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if new_status not in ['approved','rejected']:
            return Response({"message":"appointment can be approved or reject only."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        appointments.status = new_status
        appointments.save()
        return Response({"message":"status changed sucessfully."},status=status.HTTP_200_OK)
    
from rest_framework.decorators import permission_classes, api_view


@permission_classes([IsProvider])
@api_view(['GET'])
def appointments_count(request):

    user = request.user

    try:
        provider_profile = get_object_or_404(ProviderProfile,user=user)
    
    except ProviderProfile.DoesNotExist:
        return Response({"message":"Profile doesnot exists."},status=status.HTTP_404_NOT_FOUND)
    
    pending_appointments = Appointments.objects.filter(status='pending', provider = provider_profile).count()
    completed_appointments = Appointments.objects.filter(status = 'approved', provider = provider_profile).count()
    cancelled_appointments = Appointments.objects.filter(status = 'cancelled', provider = provider_profile).count()


    return Response({
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments

    }, status=status.HTTP_200_OK)

