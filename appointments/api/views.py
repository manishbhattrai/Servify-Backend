from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CreateAppointmentSerializer, CustomerGetAppointmentsSerializer, ProviderAppointmentSerializer
from appointments.models import Appointments
from .permissions import IsCustomerOnly




class CreateAppointmentView(generics.CreateAPIView):

    queryset = Appointments.objects.all()
    serializer_class = CreateAppointmentSerializer
    permission_classes = [IsCustomerOnly]


    def perform_create(self, serializer):
        
        return serializer.save(customer = self.request.user)

class CustomerGetUpdateappointmentView(APIView):

    serializer_class = CustomerGetAppointmentsSerializer
    permission_classes = [IsCustomerOnly]

    def get(self,request):

        user = self.request.user
        appointments = Appointments.objects.filter(customer=user)

        serializer = self.serializer_class(appointments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request,*agrs, **kwargs):

        user = self.request.user
        id = self.kwargs.get('id')

        appointments = get_object_or_404(Appointments, id=id ,customer = user)

        new_status = request.data.get('status')

        if not new_status:
            return Response({"message":"status is required."},status=status.HTTP_400_BAD_REQUEST)
        
        if appointments.status != 'pending':
            return Response({"message":"only pending appointments can be cancelled."},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        if new_status != 'cancelled':
            return Response({"message":"customer has only permission to cancel the appointments."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        appointments.status = 'cancelled'
        appointments.save()

        return Response({"message":"Appointment cancelled sucessfully."},status=status.HTTP_200_OK)

class ProviderAppointmentView(APIView):

    serializer_class = ProviderAppointmentSerializer

    from services.api.permissions import IsProvider
    permission_classes = [IsProvider]


    def get(self,request,*args, **kwargs):

        provider = self.request.user
        id = self.kwargs.get('id')

        if id:

            appointments = get_object_or_404(Appointments, id=id, provider=provider)
            serializer = ProviderAppointmentSerializer(appointments)
            return Response(serializer.data, status=status.HTTP_200_OK)

        appointments = Appointments.objects.filter(provider=provider)
        serializer = ProviderAppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request ,*args, **kwargs):

        provider = self.request.user
        id = self.kwargs.get('id')

        appointments = get_object_or_404(Appointments, id=id, provider=provider)

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
